from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ContractType(models.Model):

    _inherit = "hr.contract.type"

    echelon = fields.Selection(
        [("main", "Main"), ("amendment", "Amendment")],
        string="Payment Mode",
        default="main",
    )
    max_usage = fields.Integer(
        string="Maximum Usage", default=1, required=True
    )


class Contract(models.Model):
    _inherit = "hr.contract"

    name = fields.Char(compute="_compute_name")
    employee_id = fields.Many2one(required=True)
    state = fields.Selection(copy=False)
    state_admin = fields.Text(string="Administrative state", copy=False)
    type_id = fields.Many2one(
        string="Contract Type",
        domain="[('echelon', '=', type_echelon)]",
        default="",
        copy=False,
    )  # Todo: rename translation from "Catégorie de l'employé" to "Type de Contrat"
    type_echelon = fields.Selection(
        [("main", "Main"), ("amendment", "Amendment")],
        string="Contract Type Echelon",
        copy=False,
        compute="_compute_type_echelon",
    )  # Todo: add translation "Echelone du Type de Contrat"
    count_type = fields.Integer(
        string="Contract Type Count", compute="_inital_to_latest"
    )
    index_amendment = fields.Integer(
        string="Amendment Index",
        help="'O' for main contract, '1' for it's first amendment, etc.",
        default=0,
        readonly=True,
    )
    initial_contract_id = fields.Many2one(
        comodel_name="hr.contract", string="Initial Contract", readonly=True
    )
    parent_contract_id = fields.Many2one(
        comodel_name="hr.contract",
        string="Previous Contract",
        ondelete="cascade",  # Deletion of the parent deletes the amendment
        readonly=True,
        copy=False,
    )
    child_contract_id = fields.Many2one(
        comodel_name="hr.contract",
        string="Next Contract",
        readonly=True,
        copy=False,
    )
    latest_contract_id = fields.Many2one(
        comodel_name="hr.contract",
        string="Latest Contract",
        readonly=True,
        compute="_inital_to_latest",
    )

    date_signature = fields.Date(
        string="Signature Date",
        help="Signature date of the contract.",
        copy=False,
    )
    date_mailing = fields.Date(
        string="Mailing Date", help="Mailing date of the contract.", copy=False
    )
    reason = fields.Char(string="Reason for recourse to contract")
    duration = fields.Integer(string="Duration", default=6)
    hours = fields.Float(string="Working Hours", required=True)
    hourly_wage = fields.Monetary(string="Hourly Wage", required=True)
    turnover_minimum = fields.Monetary(string="Minimum Turn-Over")
    wage = fields.Monetary(
        string="Wage",
        digits=(16, 2),
        required=True,
        track_visibility="onchange",
        help="Employee's monthly gross wage.",
        compute="_compute_wage",
        copy=False,
    )
    notes = fields.Text(copy=False)

    @api.model
    def create(self, vals):
        # #  Todo: fix error when accessing self.count_type here: "Expected singleton". Maybe because the copy function is accessed both from current and initial contract?
        # if self.count_type > self.type_id.max_usage:
        #     raise ValidationError(
        #         _(
        #             "The maximum amount of %s contracts of type '%s' has been reached"
        #             % (self.count_type, self.type_id)
        #         )
        #     )
        res = super().create(vals)
        if res.index_amendment == 0:
            res.initial_contract_id = res.id
        return res

    @api.multi
    @api.depends("employee_id", "initial_contract_id", "type_id")
    def _compute_name(self):
        for contract in self:
            contract.name = "/".join(
                filter(
                    None,
                    [
                        (contract.employee_id.name or ""),
                        (
                            contract.initial_contract_id.type_id.name
                            if contract.initial_contract_id.type_id.name
                            and contract.index_amendment > 0
                            else ""
                        ),
                        (contract.type_id.name or ""),
                    ],
                )
            )

    @api.multi
    @api.depends("index_amendment")
    def _compute_type_echelon(self):
        for contract in self:
            contract.type_echelon = (
                "main" if contract.index_amendment == 0 else "amendment"
            )

    @api.multi
    @api.depends("hours", "hourly_wage")
    def _compute_wage(self):
        for contract in self:
            contract.wage = contract.hours * contract.hourly_wage

    @api.onchange("date_start", "duration")
    def onchange_date_start_duration(self):
        if self.date_start and self.duration:
            self.date_end = self.date_start + relativedelta(
                months=self.duration
            )

    @api.onchange("date_end")
    def onchange_date_end(self):
        if self.date_start and self.date_end:
            rd = relativedelta(self.date_end, self.date_start)
            self.duration = rd.months + rd.years * 12

    @api.multi
    def create_amendment(self):
        self.ensure_one()
        latest_contract_id = self.latest_contract_id
        contract = latest_contract_id.copy(
            {
                "state": "draft",
                "type_id": self.env["hr.contract.type"]
                .search([("echelon", "=", "amendment")], limit=1)
                .id,
                "initial_contract_id": latest_contract_id.initial_contract_id.id,
                "parent_contract_id": latest_contract_id.id,
                "index_amendment": latest_contract_id.index_amendment + 1,
            }
        )
        latest_contract_id.child_contract_id = contract

        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.contract",
            "view_mode": "form",
            "res_id": contract.id,
            "target": "current",
            "context": {"form_view_initial_mode": "edit"},
        }

    @api.multi
    @api.onchange("initial_contract_id", "type_id")
    def _inital_to_latest(self):
        self.ensure_one()
        current_contract_id = self.initial_contract_id
        count_type = current_contract_id.type_id == self.type_id
        while current_contract_id.child_contract_id:
            count_type += (
                current_contract_id.child_contract_id.type_id == self.type_id
            )
            current_contract_id = current_contract_id.child_contract_id
        self.latest_contract_id = current_contract_id
        self.count_type = count_type
