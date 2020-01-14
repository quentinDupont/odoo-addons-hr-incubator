# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class Exemption(models.Model):
    _name = "hr.contribution.exemption"
    _description = "Contribution Exemption"

    name = fields.Char()
    employee_id = fields.Many2one(
        comodel_name="hr.employee", string="Employee"
    )

    contribution_exemption_reason = fields.Text(
        string="Reason for Exemption", required=False
    )
    contribution_exemption_date_start = fields.Date(
        string="Start Date of Exemption", required=False
    )
    contribution_exemption_date_end = fields.Date(
        string="End Date of Exemption", required=False
    )
