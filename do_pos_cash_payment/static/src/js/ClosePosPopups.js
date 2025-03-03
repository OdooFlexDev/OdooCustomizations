odoo.define('do_pos_cash_payment.ClosePosPopups', function (require) {
    'use strict';

    const ClosePosPopup = require('point_of_sale.ClosePosPopup');
    const Registries = require('point_of_sale.Registries');
    const { useState, useRef } = owl.hooks;
    const { useValidateCashInput } = require('point_of_sale.custom_hooks');
    const { parse } = require('web.field_utils');

    const ExtendPosClosePopup = (ClosePosPopup) =>
        class extends ClosePosPopup {
            constructor() {
                super(...arguments);
                useValidateCashInput("posclosingCashInput2");
                useValidateCashInput("posclosingCashInput3");

                // Adding state and validation for new cash details
                if (this.newCashDetails) {
                    this.state.payments[this.newCashDetails.id] = {
                        counted: 0,
                        difference: -this.newCashDetails.amount,
                    };
                    useValidateCashInput("closingCashInput_" + this.newCashDetails.id, this.state.payments[this.newCashDetails.id].counted);
                }

                // Adding state and validation for cashDetails3
                if (this.cashDetails3) {
                    this.state.payments[this.cashDetails3.id] = {
                        counted: 0,
                        difference: -this.cashDetails3.amount,
                    };
                    useValidateCashInput("closingCashInput_" + this.cashDetails3.id, this.state.payments[this.cashDetails3.id].counted);
                }
            }
            
            async closeSession() {
                if (this.canCloseSession() && !this.closeSessionClicked) {
                    this.closeSessionClicked = true;
                    let response;
                    // If there are orders in the db left unsynced, we try to sync.
                    await this.env.pos.push_orders_with_closing_popup();
                    let counted_cash = 0;

                    if (this.cashControl) {
                        counted_cash += this.state.payments[this.defaultCashDetails.id].counted;
                        if (this.newCashDetails) {
                            counted_cash += this.state.payments[this.newCashDetails.id].counted;
                        }
                        if (this.cashDetails3) {
                            counted_cash += this.state.payments[this.cashDetails3.id].counted;
                        }
                        response = await this.rpc({
                            model: 'pos.session',
                            method: 'post_closing_cash_details',
                            args: [this.env.pos.pos_session.id],
                            kwargs: {
                                counted_cash: counted_cash,
                            }
                        });
                        if (!response.successful) {
                            return this.handleClosingError(response);
                        }
                    }

                    await this.rpc({
                        model: 'pos.session',
                        method: 'update_closing_control_state_session',
                        args: [this.env.pos.pos_session.id, this.state.notes]
                    });

                    try {
                        const bankPaymentMethodDiffPairs = this.otherPaymentMethods
                            .filter((pm) => pm.type === 'bank')
                            .map((pm) => [pm.id, this.state.payments[pm.id].difference]);

                        response = await this.rpc({
                            model: 'pos.session',
                            method: 'close_session_from_ui',
                            args: [this.env.pos.pos_session.id, bankPaymentMethodDiffPairs],
                            context: this.env.session.user_context,
                        });
                        if (!response.successful) {
                            return this.handleClosingError(response);
                        }
                        window.location = '/web#action=point_of_sale.action_client_pos_menu';
                    } catch (error) {
                        const iError = identifyError(error);
                        if (iError instanceof ConnectionLostError || iError instanceof ConnectionAbortedError) {
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Network Error'),
                                body: this.env._t('Cannot close the session when offline.'),
                            });
                        } else {
                            await this.showPopup('ErrorPopup', {
                                title: this.env._t('Closing session error'),
                                body: this.env._t(
                                    'An error has occurred when trying to close the session.\n' +
                                    'You will be redirected to the back-end to manually close the session.')
                            });
                            window.location = '/web#action=point_of_sale.action_client_pos_menu';
                        }
                    }
                    this.closeSessionClicked = false;
                }
            }

            handleInputChange(paymentId, event) {
                if (event.target.classList.contains('invalid-cash-input')) return;
                let expectedAmount;

                if (this.defaultCashDetails && paymentId === this.defaultCashDetails.id) {
                    this.manualInputCashCount = true;
                    this.state.notes = '';
                    expectedAmount = this.defaultCashDetails.amount;
                } else if (this.newCashDetails && paymentId === this.newCashDetails.id) {
                    this.manualInputCashCount = true;
                    this.state.notes = '';
                    expectedAmount = this.newCashDetails.amount;
                } else if (this.cashDetails3 && paymentId === this.cashDetails3.id) {
                    this.manualInputCashCount = true;
                    this.state.notes = '';
                    expectedAmount = this.cashDetails3.amount;
                } else {
                    expectedAmount = this.otherPaymentMethods.find(pm => paymentId === pm.id).amount;
                }

                this.state.payments[paymentId].counted = parse.float(event.target.value);
                this.state.payments[paymentId].difference =
                    this.env.pos.round_decimals_currency(this.state.payments[paymentId].counted - expectedAmount);
                this.state.acceptClosing = false;
            }
        };

    Registries.Component.extend(ClosePosPopup, ExtendPosClosePopup);

    return ClosePosPopup;
});
