# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class CreateAmendmentWizard(models.TransientModel):
    _name = "hr.contract.amendment.wizard"
    _description = "Create Contract Amendment"

    contract_id = fields.Many2one(
        comodel_name="hr.contract", string="Amendment of", readonly=True
    )
    latest_contract_id = fields.Many2one(
        comodel_name="hr.contract",
        string="Latests contract",
        related="contract_id.latest_contract_id",
    )
    type_id = fields.Many2one(
        comodel_name="hr.contract.type",
        string="Contract Type",
        domain="[('echelon', '=', 'amendment')]",
        required=True,
        default="",
        copy=False,
    )

    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        contract_id = self.env.context["active_id"]
        defaults["contract_id"] = contract_id
        return defaults

    @api.multi
    def create_amendment(self):
        self.ensure_one()
        _logger.info("Creating %s Amendment" % self.type_id.name)

        latest_contract_id = self.latest_contract_id
        contract = latest_contract_id.copy(
            {
                "state": "draft",
                "type_id": self.type_id.id,
                "duration": False,
                "date_end": False,
                "initial_contract_id": latest_contract_id.initial_contract_id.id,
                "parent_contract_id": latest_contract_id.id,
                "amendment_index": latest_contract_id.amendment_index + 1,
            }
        )
        latest_contract_id.child_contract_id = contract
        contract._check_contract_type_count()

        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.contract",
            "view_mode": "form",
            "res_id": contract.id,
            "target": "current",
            "context": {"form_view_initial_mode": "edit"},
        }
