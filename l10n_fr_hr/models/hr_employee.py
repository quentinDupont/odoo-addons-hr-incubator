# Copyright 2020 GRAP
# Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    country_department_of_birth_id = fields.Many2one(
        "res.country.department",
        string="French Department of Birth",
        required=False,
    )