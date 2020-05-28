# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    contract_ids = fields.One2many(
        comodel_name="hr.contract",
        inverse_name="employee_id",
        string="Contracts",
    )
    ongoing_contract_type_ids = fields.Many2many(
        comodel_name="hr.contract.type",
        string="Ongoing Contract Types",
        compute="_compute_ongoing_contract_type_ids",
        store=True,
    )

    @api.multi
    @api.depends("contract_ids", "contract_ids.state", "contract_ids.type_id")
    def _compute_ongoing_contract_type_ids(self):
        for employee in self:
            employee.ongoing_contract_type_ids = (
                employee.contract_ids.filtered(
                    lambda c: c.state in ["open", "pending"]
                    and c.echelon in ["main", "amendment"]
                )
                .mapped("type_id")
                .sorted(lambda t: t.sequence)
            )
