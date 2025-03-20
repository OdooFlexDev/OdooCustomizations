odoo.define('do_pos_combo_product.do_pos_combo_products', function (require) {
    "use strict";
   var models = require('point_of_sale.models');
   models.load_fields('product.product', 'combo_ok');
var _super_orderline = models.Orderline.prototype;
models.Orderline = models.Orderline.extend({
    export_for_printing: function() {
        var line = _super_orderline.export_for_printing.apply(this,arguments);
        line.combo_ok = this.get_product().combo_ok;
        line.required_products=this.required_product;
        line.non_required_products=this.non_required_product;
        return line;
    },
});   //Add the customisation code
});