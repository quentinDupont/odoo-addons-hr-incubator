from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ContractType(models.Model):

    _inherit = "hr.contract.type"

    echelon = fields.Selection(
        [("main", "Main"), ("amendment", "Amendment")],
        string="Echelon",
        default="main",
    )
    max_usage = fields.Integer(string="Maximum Usage", default=False)


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
        store=True,
    )  # Todo: add translation "Echelone du Type de Contrat"
    contract_type_count = fields.Integer(
        string="Contract Type Count", compute="_compute_info_inital_to_latest"
    )

    # This entire logic was written starting from the need to know
    # a contracts previous and next amendment.
    # This could be refacted by creating a model 'contract.group' containing
    # all contracts following from the parent contract, and each contract
    # could then point to that group.
    amendment_index = fields.Integer(
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
        compute="_compute_info_inital_to_latest",
    )
    all_contract_ids = fields.Many2many(
        comodel_name="hr.contract",
        string="Field Name",
        compute="_compute_info_inital_to_latest",
    )

    date_signature = fields.Date(
        string="Signature Date",
        help="Signature date of the contract.",
        copy=False,
    )
    date_mailing = fields.Date(
        string="Mailing Date", help="Mailing date of the contract.", copy=False
    )
    reason = fields.Char(string="Reason for recourse to contract", copy=False)
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
    )
    notes = fields.Text(copy=False)

    attachment_number = fields.Integer(
        compute="_compute_attachment_number", string="Number of Attachments"
    )
    attachment_ids = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        string="Attachments",
        domain=[("res_model", "=", "hc.contract")],
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.amendment_index == 0:
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
                            if contract.amendment_index > 0
                            else ""
                        ),
                        (
                            str(contract.amendment_index)
                            if contract.amendment_index > 0
                            else ""
                        ),
                        (contract.type_id.name or ""),
                    ],
                )
            )

    @api.multi
    @api.depends("amendment_index")
    def _compute_type_echelon(self):
        for contract in self:
            contract.type_echelon = (
                "main" if contract.amendment_index == 0 else "amendment"
            )

    @api.multi
    @api.depends("hours", "hourly_wage")
    def _compute_wage(self):
        for contract in self:
            contract.wage = contract.hours * contract.hourly_wage

    @api.onchange("date_start", "duration")
    def onchange_date_start_duration(self):
        if not self.duration:
            self.date_end = False
        if self.date_start and self.duration:
            self.date_end = self.date_start + relativedelta(
                months=self.duration
            )

    @api.onchange("date_end")
    def onchange_date_end(self):
        if not self.date_end:
            self.duration = False
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
                "duration": False,
                "date_end": False,
                "initial_contract_id": latest_contract_id.initial_contract_id.id,
                "parent_contract_id": latest_contract_id.id,
                "amendment_index": latest_contract_id.amendment_index + 1,
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
    @api.depends("initial_contract_id", "type_id")
    def _compute_info_inital_to_latest(self):
        for contract in self:
            current_contract_id = contract.initial_contract_id
            # all_contract_ids = [current_contract_id.id]
            # todo: fix error when computing id's and restore functionnality
            contract_type_count = (
                current_contract_id.type_id == contract.type_id
            )  # todo: cast to integer or use if
            while current_contract_id.child_contract_id:
                # all_contract_ids.append(
                #     current_contract_id.child_contract_id.id
                # )
                contract_type_count += (
                    current_contract_id.child_contract_id.type_id
                    == contract.type_id
                )  # todo: cast to integer or use if
                current_contract_id = current_contract_id.child_contract_id
            contract.latest_contract_id = current_contract_id
            # contract.all_contract_ids = [(6, 0, all_contract_ids)]
            contract.contract_type_count = contract_type_count

    @api.multi
    def _compute_attachment_number(self):
        read_group_res = self.env["ir.attachment"].read_group(
            [("res_model", "=", "hr.contract"), ("res_id", "in", self.ids)],
            ["res_id"],
            ["res_id"],
        )
        attach_data = {
            res["res_id"]: res["res_id_count"] for res in read_group_res
        }
        for contract in self:
            contract.attachment_number = attach_data.get(contract.id, 0)

    @api.multi
    def action_get_attachment_tree_view(self):
        self.ensure_one()
        attachment_action = self.env.ref("base.action_attachment")
        action = attachment_action.read()[0]
        action["context"] = {
            "default_res_model": self._name,
            "default_res_id": self.ids[0],
        }
        action["domain"] = str(
            ["&", ("res_model", "=", self._name), ("res_id", "in", self.ids)]
        )
        return action

    @api.multi
    @api.constrains("contract_type_count", "type_id")
    def _check_contract_type_count(self):
        for contract in self:
            if (
                contract.type_id.max_usage
                and contract.contract_type_count > contract.type_id.max_usage
            ):
                raise ValidationError(
                    _(
                        "The maximum amount of %s contracts "
                        "of type '%s' has been reached"
                        % (contract.type_id.max_usage, contract.type_id.name)
                    )
                )
