odoo.define('do_pos_customization.TicketScreen', function(require) {
    "use strict";

    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');

    const PosTicketScreen = TicketScreen => class extends TicketScreen {
        constructor() {
            super(...arguments);
        }

        _autoUpdateRefundqty() {
            const order = this.getSelectedSyncedOrder();
            if (!order) {
                return;
            }
            for (const o_idx in order.orderlines.models) {
                const orderline = order.orderlines.models[o_idx];
                const toRefundDetail = this._getToRefundDetail(orderline);
                const refundableQty = orderline.get_quantity() - orderline.refunded_qty;
                if (refundableQty > 0) {
                    toRefundDetail.qty = refundableQty;
                }
            }
        }

    //@override    
    async _onDoRefund() {
        const order = this.getSelectedSyncedOrder();
        console.log("getSelectedSyncedOrder===",order);
        if (!order) {
            this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
            return this.render();
        }

        if (this._doesOrderHaveSoleItem(order)) {
            this._prepareAutoRefundOnOrder(order);
        }

        const customer = order.get_client();

        const allToRefundDetails = this._getRefundableDetails(customer)
        if (allToRefundDetails.length == 0) {
            this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
            this._autoUpdateRefundqty();
            return this._onDoRefund();
        }
        // The order that will contain the refund orderlines.
        // Use the destinationOrder from props if the order to refund has the same
        // customer as the destinationOrder.
        const destinationOrder = this._setDestinationOrder(this.props.destinationOrder, customer);
        //Add a check too see if the fiscal position exist in the pos
        if (order.fiscal_position_not_found) {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Fiscal Position not found'),
                body: this.env._t('The fiscal position used in the original order is not loaded. Make sure it is loaded by adding it in the pos configuration.')
            });
            return;
        }

        // Add orderline for each toRefundDetail to the destinationOrder.
        for (const refundDetail of allToRefundDetails) {
            const product = this.env.pos.db.get_product_by_id(refundDetail.orderline.productId);
            const options = this._prepareRefundOrderlineOptions(refundDetail);
            await destinationOrder.add_product(product, options);
            refundDetail.destinationOrderUid = destinationOrder.uid;
        }

        destinationOrder.fiscal_position = order.fiscal_position;
        // Set the customer to the destinationOrder.
        if (customer && !destinationOrder.get_client()) {
            destinationOrder.set_client(customer);
            destinationOrder.updatePricelist(customer);
        }

        this._onCloseScreen();
    }
    };



    Registries.Component.extend(TicketScreen, PosTicketScreen);

    return TicketScreen;
});
