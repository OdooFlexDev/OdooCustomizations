/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { jsonrpc } from "@web/core/network/rpc_service";

class SalonKiosk extends Component {
    setup() {
        this.services = [];
        this.appointment = useState({name : '', waiting_time : 0})
        this.state = useState({showSuccessMessage:false});
        this.state = useState({existing_user:false});
        this.users = [];
        this.formData = useState({
            client_name: '',
            phone_number: '',
            email: '',
            service_ids: [], 
            terms_accepted: false
        });
        onWillStart(async () => {
            await this.getServices();
            await this.getUsers();
            this.render();
        });
    }
    async getUsers() {
        const users = await jsonrpc('/web/dataset/call_kw/res.partner/search_read', {
            model: "res.partner",
            method: "search_read",
            args: [{}],
            kwargs: {},
        });
        this.users = users;
    }
    async getServices() {
        const services = await jsonrpc('/web/dataset/call_kw/product.product/search_read', {
            model: "product.product",
            method: "search_read",
            args: [[['salon_ok', '=', true]]],
            kwargs: {},
        });
        this.services = services;
    }
    async handleCheckboxChange(event){
        this.state.existing_user = event.target.checked;
    }

    async handleSubmit(event) {
        event.preventDefault();

        if (!this.state.existing_user){
                const { client_name, phone_number, email, service_ids, terms_accepted } = this.formData;
                // Check if any fields are missing
                if (!client_name || !phone_number || !email || !service_ids.length || !terms_accepted) {
                    alert("Please fill out all fields, select services, and accept the terms.");
                    return;
                }

                // Validate phone number (example: allows only numbers, spaces, dashes, parentheses)
                const phoneRegex = /^\+?[1-9]\d{7,14}$/;
                if (!phoneRegex.test(phone_number)) {
                    alert("Please enter a valid phone number.");
                    return;
                }

                // Validate email format
                const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
                if (!emailRegex.test(email)) {
                    alert("Please enter a valid email address.");
                    return;
                }
                // Call the search_and_create method with the form data
                const [checkin, waitingTime] = await jsonrpc('/web/dataset/call_kw/salon.client.checkin/search_and_create', {
                    model: "salon.client.checkin",
                    method: "search_and_create",
                    args: [],
                    kwargs: {
                        'name': client_name,
                        'phone': phone_number,
                        'email': email,
                        'service_ids': service_ids,
                        'terms_accepted': terms_accepted,
                    },
                });
                this.appointment.name = checkin;
                this.appointment.waiting_time = waitingTime;
                // Clear the form data after submission
                this.formData.client_name = '';
                this.formData.phone_number = '';
                this.formData.email = '';
                this.formData.service_ids = [];
                this.formData.terms_accepted = false;
                this.state.showSuccessMessage = true;
            }    
        else{
            const { phone_number, service_ids, terms_accepted} = this.formData;
                const [checkin, waitingTime] = await jsonrpc('/web/dataset/call_kw/salon.client.checkin/search_and_create', {
                    model: "salon.client.checkin",
                    method: "search_and_create",
                    args: [],
                    kwargs: {
                        'name': null,
                        'phone': phone_number,
                        'email': null,
                        'service_ids': service_ids,
                        'terms_accepted': terms_accepted,
                    },
                });
                this.appointment.name = checkin;
                this.appointment.waiting_time = waitingTime;
                this.formData.phone_number = '';
                this.formData.service_ids = [];
                this.formData.terms_accepted = false;
                this.state.showSuccessMessage = true;
        }
    }


    restartForm() {
        this.state.showSuccessMessage = false;
        this.render();
    }
    // Function to handle checking/unchecking of services
      async handleServiceChange(event) {
            const checked = event.target.checked;
            const serviceId = event.target.value;
            if (checked) {
                this.formData.service_ids.push(serviceId);
            } else {
                const index = this.formData.service_ids.indexOf(serviceId);
                if (index > -1) {
                    this.formData.service_ids.splice(index, 1);
                }
            }
        }

}

SalonKiosk.template = "do_salon_kiosk_app.salonaction";

registry.category("actions").add("do_salon_kiosk_app.SalonKioskModeAction", SalonKiosk);
export default SalonKiosk;
