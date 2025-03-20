from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_quant import StockQuant
from odoo.tools.float_utils import float_compare


class InventoryAdjustmentDate(models.Model):
    _inherit = 'stock.quant'

    def _apply_inventory(self):
        move_vals = []
        inventories = self.env['stock.quant']
        main_date = self.accounting_date

        # Calling the super method with the adjusted context
        super(InventoryAdjustmentDate, inventories.with_context(force_period_date=main_date))._apply_inventory()

        # Check if the user has the right access level
        if not self.user_has_groups('stock.group_stock_manager'):
            raise UserError(_('Only a stock manager can validate an inventory adjustment.'))

        for quant in self:
            # Check if inventory_diff_quantity is positive or negative and create corresponding move values
            if float_compare(quant.inventory_diff_quantity, 0, precision_rounding=quant.product_uom_id.rounding) > 0:
                move_vals.append(
                    quant._get_inventory_move_values(quant.inventory_diff_quantity,
                                                     quant.product_id.with_company(quant.company_id).property_stock_inventory,
                                                     quant.location_id)
                )
            else:
                move_vals.append(
                    quant._get_inventory_move_values(-quant.inventory_diff_quantity,
                                                     quant.location_id,
                                                     quant.product_id.with_company(quant.company_id).property_stock_inventory,
                                                     out=True)
                )

        # Create the moves and perform the action
        moves = self.env['stock.move'].with_context(inventory_mode=False).create(move_vals)
        moves.with_context(force_period_date=main_date)._action_done()

        # Update location's last inventory date
        self.location_id.write({'last_inventory_date': quant.accounting_date})

        # Prepare next inventory date for each location
        date_by_location = {loc: loc._get_next_inventory_date() for loc in self.mapped('location_id')}
        
        for quant in self:
            # Set inventory date per location
            quant.inventory_date = date_by_location[quant.location_id]

        # Update the move's date to the accounting date
        move = self.env['stock.move'].search([('id', '=', moves.id)])
        move.date = main_date
        for move_lines in move.move_line_ids:
            move_lines.date = quant.accounting_date

        # Update the stock valuation layer's creation date
        for moves in move:
            self.env.cr.execute(
                "UPDATE stock_valuation_layer SET create_date = (%s) WHERE stock_move_id = %s",
                [main_date, int(moves.id)]
            )

        # Reset quant's inventory-related fields
        self.write({
            'inventory_quantity': 0,
            'user_id': False,
            'inventory_diff_quantity': 0,
            'accounting_date': 0
        })


class InheritApplyToAll(models.TransientModel):
    _inherit = "stock.inventory.adjustment.name"

    def action_apply(self):
        # Check if more than one quant is selected
        if len(self.quant_ids.ids) > 1:
            raise UserError(_('Change Effective Date is installed and can\'t handle applying to multiple records'))
        elif len(self.quant_ids.ids) != 0:
            # Apply the inventory adjustment to the selected quant
            InventoryAdjustmentDate._apply_inventory(self.quant_ids)
