# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    expiration_date = fields.Date(string="Expiration Date", required=False)
