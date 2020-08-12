# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
#   Robin Keunen <robin@coopiteasy.be>
# Copyright 2020 GRAP
#   Quentin Dupont <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Contract(models.Model):
    _inherit = "hr.contract"

    turnover_minimum = fields.Monetary(string="Minimum Turn-Over")

    @api.onchange("employee_id")
    def onchange_employee_id(self):
        # import pdb; pdb.set_trace();
        super().onchange_employee_id()
        # if self.employee_id.turnover_minimum:
        self.turnover_minimum = self.employee_id.turnover_minimum