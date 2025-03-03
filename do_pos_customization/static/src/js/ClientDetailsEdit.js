odoo.define('do_pos_customization.ClientDetailsEdit', function(require) {

    const ClientDetailsEdit = require('point_of_sale.ClientDetailsEdit');
    const Registries = require('point_of_sale.Registries');
    const FleetClientDetailsEdit = ClientDetailsEdit => class extends ClientDetailsEdit {
        constructor() {
            super(...arguments);
            this.intFields.push("fleet_id");
            this.changes.fleet_id = this.props.partner.fleet_id && this.props.partner.fleet_id[0];
        }
    };

    Registries.Component.extend(ClientDetailsEdit, FleetClientDetailsEdit);

    return ClientDetailsEdit;
});
