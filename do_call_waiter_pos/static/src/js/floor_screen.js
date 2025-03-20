import { patch } from "@web/core/utils/patch";
import { FloorScreen } from "@pos_restaurant/app/floor_screen/floor_screen";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { rpc } from "@web/core/network/rpc";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(FloorScreen.prototype, {
	setup() {
		super.setup();
		var self = this
		new BroadcastChannel("call_waiter_notify").onmessage = (event) => {
			self.setCallWaiterNotify(event.data)
		};
	},

	async onClickTable(table, ev) {
		var self = this
		const Tables = this.env.services.pos_data.indexedRecords['restaurant.table'].id
		var CurrentTable;
		for (const loop_table of Object.values(Tables)) {
			if (loop_table.table_number === table.table_number) {
				CurrentTable = loop_table
			}
		}
		var response = await rpc("/check/active_tables/", { "floor_id": this.activeFloor.id, "table": CurrentTable.id })
		if (response.data) {
			self.dialog.add(ConfirmationDialog,{
				title: _t("Information"),
				body: "Waiter Call From " + CurrentTable.table_number,
			});
		}
		if (this.pos.isEditMode) {
			if (this.state.selectedTableIds.includes(table.id)) {
				this.state.selectedTableIds = this.state.selectedTableIds.filter(
					(id) => id !== table.id
				);
				return;
			}
			if (!ev.ctrlKey && !ev.metaKey) {
				this.unselectTables();
			}
			this.state.selectedTableIds.push(table.id);
			return;
		}
		if (table.parent_id) {
			this.onClickTable(table.parent_id, ev);
			return;
		}
		if (!this.pos.isOrderTransferMode) {
			await this.pos.setTableFromUi(table);
		}
	},

	async setCallWaiterNotify(data) {
		var tablename = data.tablename
		var tableid = data.tableid
		var time = data.time
		var self = this
		const Tables = this.env.services.pos_data.indexedRecords['restaurant.table'].id
		const infoDivs = document.querySelectorAll('div.info');
		infoDivs.forEach(async div => {
			const labelDiv = div.querySelector('.label');
			const value = labelDiv ? labelDiv.innerText : null;
			if (value == tablename) {
				div.style.border = '5px solid pink';
				for (const table of Object.values(Tables)) {
					if (table.id === tableid) {
						data = {"table":tableid,"date":time}
						const activeFloor = self.activeFloor;
						await self.pos.data.call("restaurant.floor", "set_active_tables", [
							activeFloor.id,
							table.id,
							"add",
							data,
						]);
					}
				}
			}
		});
	}
});