odoo.define('do_pos_customization.models', function (require) {
"use strict";

var models = require('point_of_sale.models');
    models.load_fields("res.partner", ["fleet_id"]);
    models.load_models({
        model: 'fleet.vehicle',
        fields: ['name'],
        domain: [],
        loaded: function (self, datas) {
            self.fleet_vehicle = datas;
            self.fleet = {}
            _.each(datas, function (d) {
                self.fleet[d['id']] = d
            });
        },
    });
    var super_order_model = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            super_order_model.initialize.apply(this, arguments);
            this.is_cash_customer = false;
            this.cash_payment_method = this.pos.payment_methods.filter(
            (method) => this.pos.config.payment_method_ids.includes(method.id) && method.is_cash_count == true);
        },
        init_from_JSON: function (json) {
            super_order_model.init_from_JSON.apply(this, arguments);
            this.is_cash_customer = json.is_cash_customer;
        },
        export_as_JSON: function () {
            const json = super_order_model.export_as_JSON.apply(this, arguments);
            json['is_cash_customer'] = this.is_cash_customer;
            return json;
        },
    });
});

