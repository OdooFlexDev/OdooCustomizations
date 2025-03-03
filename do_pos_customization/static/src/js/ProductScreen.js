odoo.define('do_pos_customization.ProductScreen', function (require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useBarcodeReader } = require('point_of_sale.custom_hooks');
    const NumberBuffer = require('point_of_sale.NumberBuffer');

    const PosProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
            }
            get currentOrder() {
                return this.env.pos.get_order();
            }
            async _onClickPay() {
                super._onClickPay(...arguments);
                if(this.currentOrder.cash_payment_method && this.currentOrder.is_cash_customer)
                {
                    let result = this.currentOrder.add_paymentline(this.currentOrder.cash_payment_method[0]);
                    if (result){
                        NumberBuffer.reset();
                        return true;
                    }
                    else{
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Error'),
                            body: this.env._t('There is already an electronic payment in progress.'),
                        });
                        return false;
                    }
                }
                
            }
        };

    Registries.Component.extend(ProductScreen, PosProductScreen);

    return ProductScreen;
});
