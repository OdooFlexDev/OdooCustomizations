import { patch } from "@web/core/utils/patch";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(OrderSummary.prototype, {
    _setValue(val) {
    	let selectedLine = this.currentOrder.get_selected_orderline();
        
        if (this.pos.config.basic_employee_ids && this.pos.config.basic_employee_ids.some(employee => employee.id === this.pos.get_cashier().id)) {

	        if (selectedLine.get_quantity() > val && this.pos.numpadMode === "quantity") {

	            this.dialog.add(AlertDialog, {
	                title: _t("Update quantity"),
	                body: _t(
	                    "You cannot decrease quantity. Contact Manager to change Quantity."
	                ),
	            });
	            return false;
	        }
	        else if(val === "remove"){
	            this.dialog.add(AlertDialog, {
	                title: _t("Remove Product Qty"),
	                body: _t(
	                    "You cannot remove product quantity. Contact Manager to change Quantity."
	                ),
	            });
	            return false;        	
	        }
	    }
        super._setValue(val);
    },

});
