# Copyright 2019 Coop IT Easy SCRL fs
# Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    # Columns Section
    mutual_insurance_state = fields.Selection(
        [
            ("affiliated", "Affiliated"),
            ("exempted", "Exempted"),
            ("dontknowyet", "Don't know yet"),
        ],
        string="State for Mutual Insurance",
        default="dontknowyet",
        required=True,
        help="Help to know if this employee should have Mutual",
    )

    mutual_insurance_proof_received = fields.Boolean(
        string="Proof received", default=False
    )

    show_status_origin = fields.Boolean(
        string="Show Status Origin", default=False
    )

    disabled_worker_status = fields.Boolean(
        string="Disabled Worker Status", default=False
    )

    disabled_worker_attachment = fields.Boolean(
        string="Disabled Worker Attachment", default=False
    )

    # compute section
    @api.onchange("disabled_worker_status")
    def onchange_disabled_worker_status(self):
        if self.disabled_worker_status is False:
            self.disabled_worker_attachment = False
