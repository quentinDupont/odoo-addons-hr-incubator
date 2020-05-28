# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    contribution_date_start = fields.Date(
        string="Start Date of Contributions", required=False
    )
    # contribution_arrangements = fields.Selection(
    #     related="partner_id.contribution_arrangements"
    # ) # Todo: field will be available from Scopa in partner_id
    # fixme should be Many2One
    contribution_exemption_ids = fields.One2many(
        comodel_name="hr.contribution.exemption",
        inverse_name="employee_id",
        string="Contribution Exemptions",
        required=False,
    )
