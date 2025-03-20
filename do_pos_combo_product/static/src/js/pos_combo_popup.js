/** @odoo-module **/
import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { useListener } from 'web.custom_hooks';
const { useState } = owl.hooks;

class ComboProductsPopup extends AbstractAwaitablePopup {
    constructor() {
        super(...arguments);
        this.selectedProductIds = []; // Store selected product IDs here
    }

    async _onClickProduct(ev) {
        const productElement = $(ev.target).closest('.product-card');
        const selectedLabel = productElement.find('.selected');
        selectedLabel.toggle();
        const productId = selectedLabel.data('product-id');
        const itemCount = this.props.item_count;
        const selectedCount = $('.product-card .selected:visible').length;

        if (selectedCount > itemCount) {
            alert('Selected items exceed item count. Please deselect some items.');
            selectedLabel.toggle(); // Revert the selection
        } else {
            // Add or remove the selected product ID from the array
            if (selectedLabel.is(':visible')) {
                this.selectedProductIds.push(productId);
            } else {
                const index = this.selectedProductIds.indexOf(productId);
                if (index !== -1) {
                    this.selectedProductIds.splice(index, 1);
                }
            }
        }
    }

    // Export the selected product IDs
    getPayload() {
        return this.selectedProductIds;
    }
}

// Create products popup
ComboProductsPopup.template = 'ComboProductsPopup';
ComboProductsPopup.defaultProps = {
    confirmText: 'Ok',
    cancelText: 'Cancel',
    title: 'Combo Products',
    body: '',
};
Registries.Component.add(ComboProductsPopup);

export default ComboProductsPopup;
