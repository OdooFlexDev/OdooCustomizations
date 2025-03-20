import { OrderWidget } from "@pos_self_order/app/components/order_widget/order_widget";
import { patch } from "@web/core/utils/patch";

patch(OrderWidget.prototype, {
	CallWaiter() {
		const selfOrder = this.selfOrder;
		var CurrentTable = this.selfOrder.currentTable
		const tableName = CurrentTable.table_number;
		const tableid = CurrentTable.id;
		const time = new Date().toLocaleTimeString();
		const customerDisplayData = {'tablename': tableName,'tableid':tableid,'time': time}
		var customerDisplayChannel = new BroadcastChannel("call_waiter_notify");
		customerDisplayChannel.postMessage(customerDisplayData);
	}
});