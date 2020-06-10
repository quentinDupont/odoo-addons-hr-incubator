# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    employee_ids = fields.Many2many(
        comodel_name="hr.employee",
        string="Entrepreneurs assisted during this timeslot",
    )
