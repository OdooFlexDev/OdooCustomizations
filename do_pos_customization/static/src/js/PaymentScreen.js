odoo.define('do_pos_customization.PaymentScreen', function(require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const { onMounted } = owl.hooks;
    const PosPaymentScreen = PaymentScreen => class extends PaymentScreen {
        constructor() {
            super(...arguments);
            onMounted(() => {
                if (this.currentOrder.is_cash_customer && this.currentOrder.get_due() == 0) {                    
                    this.validateOrder(true);
                }
            });
        }
    };

    Registries.Component.extend(PaymentScreen, PosPaymentScreen);

    return PaymentScreen;
});
