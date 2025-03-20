# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import AccessDenied

class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_vendor_ids = fields.Many2many(
        'res.partner',
        string='Allowed Vendors',
        domain="[('supplier_rank', '>', 0)]",
        help="List of vendors this user is allowed to see in Purchase Orders."
    )
    passcode = fields.Char(required=True, string="Passcode", help="Used to log into the system")

    def _check_credentials(self, passcode, env):
        """ Validates the current user's password.

        Override this method to plug additional authentication methods.

        Overrides should:

        * call `super` to delegate to parents for credentials-checking
        * catch AccessDenied and perform their own checking
        * (re)raise AccessDenied if the credentials are still invalid
          according to their own validation method

        When trying to check for credentials validity, call _check_credentials
        instead.
        """
        """ Override this method to plug additional authentication methods"""
        assert passcode
        self.env.cr.execute(
            "SELECT COALESCE(passcode, '') FROM res_users WHERE id=%s",
            [self.env.user.id]
        )
        [hashed] = self.env.cr.fetchone()
        valid, replacement = self._crypt_context()\
            .verify_and_update(passcode, hashed)
        if replacement is not None:
            self._set_encrypted_password(self.env.user.id, replacement)
        if not valid:
            raise AccessDenied()

