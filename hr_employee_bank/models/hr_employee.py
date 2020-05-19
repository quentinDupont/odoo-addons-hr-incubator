# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
#   Robin Keunen <robin@coopiteasy.be>
# Copyright 2020 GRAP
#   Quentin Dupont <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    bank_account_payment_id = fields.Many2one(
        "res.partner.bank",
        string="Bank Account Number for Payment",
        required=False,
        domain="[('partner_id', '=', address_home_id)]",
        help="Employee bank salary account",
    )
    valid_mandate_id = fields.Many2one(
        related="user_id.partner_id.valid_mandate_id"
    )
