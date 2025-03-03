odoo.define('do_pos_customization.CashCustomerButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require('web.custom_hooks');

    class CashCustomerButton extends PosComponent {
        constructor() {        
        super(...arguments);
    }
    get currentOrder() {
        return this.env.pos.get_order();
    }

    get is_cash_customer() {
        return this.currentOrder ? this.currentOrder.is_cash_customer : false;
    }

    async onClick() {
         this.currentOrder.is_cash_customer = !this.currentOrder.is_cash_customer;
         if (this.currentOrder.is_cash_customer){
             document.getElementById("cash_button").style.background = "lightblue";
         }
         else{
            document.getElementById("cash_button").style.backgroundColor = "";
         }
    }
    }
    CashCustomerButton.template = 'CashCustomerButton';

    ProductScreen.addControlButton({
        component: CashCustomerButton,
        condition: function () {
            return true;
        },
    });

    Registries.Component.add(CashCustomerButton);

    return CashCustomerButton;
});
