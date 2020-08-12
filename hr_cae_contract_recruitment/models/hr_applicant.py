# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
#   Robin Keunen <robin@coopiteasy.be>
# Copyright 2020 GRAP
#   Quentin Dupont <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Applicant(models.Model):
    _inherit = "hr.applicant"

    currency_id = fields.Many2one(
        string="Currency", related="company_id.currency_id", readonly=True
    )
    turnover_minimum = fields.Monetary(string="Minimum Turn-Over")

    @api.multi
    def create_employee_from_applicant(self):
        employee_action_window = super().create_employee_from_applicant()
        # note: this function does not use `ensure_one`. It returns the
        # action window on the last created employee.
        for applicant in self:
            employee = applicant.emp_id
            employee.turnover_minimum = applicant.turnover_minimum

        return employee_action_window
