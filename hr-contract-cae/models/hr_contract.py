from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class Contract(models.Model):

    _inherit = "hr.contract"

    reason = fields.Char(string="Reason for recourse to contract")

    duration = fields.Integer(string="Duration", default=6)
    date_end = fields.Date(
        "End Date", help="End date of the contract (if it's a fixed-term contract)."
    )

    hours = fields.Float(string="Working Hours", required=True)
    rate = fields.Monetary(string="Hourly Rate", required=True)

    turnover_minimum = fields.Monetary(string="Minimum Turn-Over")

    wage = fields.Monetary(
        "Wage",
        digits=(16, 2),
        required=True,
        track_visibility="onchange",
        help="Employee's monthly gross wage.",
        compute="_compute_wage",
    )

    @api.multi
    @api.depends("hours", "rate")
    def _compute_wage(self):
        for contract in self:
            contract.wage = self.hours * self.rate

    @api.onchange("date_start", "duration")
    def onchange_date_start_duration(self):
        if self.date_start and self.duration:
            self.date_end = self.date_start + relativedelta(months=self.duration)

    @api.onchange("date_end")
    def onchange_date_end(self):
        if self.date_start and self.date_end:
            self.duration = relativedelta(self.date_end, self.date_start).months
