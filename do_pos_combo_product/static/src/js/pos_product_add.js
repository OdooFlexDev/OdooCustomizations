odoo.define('do_pos_combo_product.ProductScreen_do_pos_combo_product', function(require) {
   'use strict';
   const Registries = require('point_of_sale.Registries');
   const ProductScreen = require('point_of_sale.ProductScreen');
   var rpc = require('web.rpc');

   const PosComboProduct = (ProductScreen) => class extends ProductScreen {

        async _clickProduct(event) {
            if (!this.currentOrder) {
                this.env.pos.add_new_order();
            }
            const product = event.detail;
            const options = await this._getAddProductOptions(product);

            // Initialize category_non variable
            let category_non;
            let item_count;
            let category_req;
            // Check if the product is marked as "combo_ok"
            if (product.combo_ok) {
                const comboData = await this.rpc({
                        model: 'product.product',
                        method: 'get_combo_data',
                        args: [product.id],
                });

                const requiredProducts = [];
                const nonRequiredProducts = [];

                // Assuming comboData is an array of objects
                comboData.forEach(combo => {
                    if (combo.is_required) {
                        for (let i = 0; i < combo.product_names.length; i++) {
                            category_req=combo.pos_category_name;
                            requiredProducts.push({
                                pos_category_id: combo.pos_category_id,
                                product_img: combo.product_img[i],
                                product_ids: combo.product_ids[i],
                                product_name: combo.product_names[i],
                                is_required: combo.is_required,
                                item_count: combo.item_count,
                            });
                        }
                    } else {
                        for (let i = 0; i < combo.product_names.length; i++) {
                            category_non = combo.pos_category_name; // Assign value to category_non
                            item_count = combo.item_count;
                            nonRequiredProducts.push({
                                pos_category_id: combo.pos_category_id,
                                product_img: combo.product_img[i],
                                product_name: combo.product_names[i],
                                product_ids: combo.product_ids[i],
                                is_required: combo.is_required,
                            });
                        }
                    }
                });
                const { confirmed,payload:product_id } = await this.showPopup('ComboProductsPopup', {
                    title: product.display_name,
                    requiredProducts: requiredProducts,
                    nonRequiredProducts: nonRequiredProducts,
                    category_non: category_non, // Use category_non here
                    item_count:item_count,
                    category_req:category_req,
                });
                if (confirmed) {
                    this.currentOrder.add_product(product, options);
                    const requiredProductObjs = [];
                    const nonRequiredProductObjs=[];
                    for (const requiredProduct of requiredProducts) {
                        const requiredProductObj = this.env.pos.db.get_product_by_id(requiredProduct.product_ids);
                        requiredProductObjs.push(requiredProductObj);
                        this.currentOrder.selected_orderline.required_product = requiredProductObjs;
                    }
                    for (const nonRequiredProduct of nonRequiredProducts) {
                        if (nonRequiredProduct.product_ids == product_id) {
                            const nonRequiredProductObj = this.env.pos.db.get_product_by_id(nonRequiredProduct.product_ids);
                            nonRequiredProductObjs.push(nonRequiredProductObj);
                             this.currentOrder.selected_orderline.non_required_product = nonRequiredProductObjs;
                        }
                    }
                }
            }
            else {
                // Add the product to the order for non-combo_ok products
                if (!options) return;
                this.currentOrder.add_product(product, options);

                try {
                    NumberBuffer.reset();
                }
                catch(err) {
                    console.log(err);
                }
            }
        }
    };
    Registries.Component.extend(ProductScreen, PosComboProduct);
});