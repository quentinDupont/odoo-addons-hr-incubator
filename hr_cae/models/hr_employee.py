# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _inherit = "hr.employee"

    country_department_id = fields.Many2one(
        "res.country.department", string="Department (France)", required=False
    )
    country_other_ids = fields.Many2many(
        "res.country", string="Other Nationalities", required=False
    )
    date_start = fields.Date(
        string="Date of Entry", default=fields.Date.today(), required=False
    )
    date_end = fields.Date(string="Date of Obsolescence")
    origin_status_id = fields.Many2one(
        "hr.origin.status", string="Origin Status", required=False
    )
    origin_status_details_id = fields.Many2one(
        "hr.origin.status.details",
        string="Origin Status Details",
        domain="[('origin_status_id', '=', origin_status_id)]",
        required=False,
    )
    certificate_id = fields.Many2one(
        "hr.recruitment.degree", string="Certificate Level", required=False
    )  # TODO: remove standard certificate field from view
    # TODO: copy from applicant_id.type_id on creation
    bank_account_payment_id = fields.Many2one(
        "res.partner.bank",
        string="Bank Account Number for Payment",
        required=False,
        domain="[('partner_id', '=', address_home_id)]",
        help="Employee bank salary account",
    )  # TODO: check that this one is actually used in logic
    coop_role_id = fields.Many2one(
        "hr.coop.role", string="Role in the cooperative", required=False
    )
    social_insurance_id = fields.Many2one(
        "hr.social.insurance", string="Social Insurance", required=False
    )
    mutual_insurance_id = fields.Many2one(
        "hr.mutual.insurance", string="Mutual Insurance", required=False
    )
    mutual_insurance_level_id = fields.Many2one(
        "hr.mutual.insurance.level", string="Mutual Insurance Level", required=False
    )
    mutual_insurance_date_start = fields.Date(
        string="Start Date of Mutual Insurance", required=False
    )
    mutual_insurance_date_end = fields.Date(
        string="End Date of Mutual Insurance", required=False
    )
    mutual_insurance_date_exemption = fields.Date(
        string="Exemption Date Mutual Insurance", required=False
    )
    medic_dispense_date = fields.Date(string="Date of Medical Dispense", required=False)
    transport_mode_id = fields.Many2one(
        "hr.transport.mode", string="Transport Mode", required=False
    )
    invalidity_rate = fields.Float(
        string="Invalidity Rate", required=False, default=0
    )  # use percentage widget
    job_other_companies = fields.Text(string="Other Employers", required=False)
    job_other_hours = fields.Float(
        string="Cumulative Other Working Hours", required=False
    )  # Todo: in xml, style as 'per month'
    job_retirement = fields.Boolean(
        string="Combining Job and Retirement", required=False
    )
    job_adaptations = fields.Text(string="Job Adaptations", required=False)
    professional_liability_ids = fields.Many2many(
        comodel_name="hr.professional.liability",
        string="Professional Liability",
        required=False,
    )
    professional_liability_insurance_policy_ref = fields.Text(
        string="Professional Liability Insurance Policy Reference", required=False
    )
    vehicle_insurance = fields.Text(string="Vehicle Insurance", required=False)
    office = fields.Text(string="Office", required=False)
    equipment = fields.Text(string="Equipment", required=False)
    sector_ids = fields.Many2many(
        comodel_name="hr.sector", string="Sector", required=False
    )
    adult_dependents = fields.Integer(string="Adult Dependents", required=False)
    social_worker = fields.Text(string="Social Worker", required=False)
    contribution_date_start = fields.Date(
        string="Start Date of Contributions", required=False
    )
    # contribution_arrangements = fields.Selection(
    #     related="partner_id.contribution_arrangements"
    # ) # Todo: field will be available from Scopa in partner_id
    contribution_exemption_reason = fields.Text(
        string="Reason for Exemption", required=False
    )
    contribution_exemption_date_start = fields.Date(
        string="Start Date of Exemption", required=False
    )
    contribution_exemption_date_end = fields.Date(
        string="End Date of Exemption", required=False
    )

    _sql_constraints = [
        (
            "check_invalidity_rate",
            "CHECK(invalidity_rate >= 0 AND invalidity_rate <= 100)",
            "The percentage of an invalidity_rate should be between 0 and 100.",
        ),
        (
            "check_job_other_hours",
            "CHECK(job_other_hours >= 0)",
            "The cumulative other working hours should greater then or equal to 0.",
        ),
        (
            "check_adult_dependents",
            "CHECK(adult_dependents >= 0)",
            "The number of Adult Dependents should greater then or equal to 0.",
        ),
    ]

    @api.constrains("date_start", "date_end")
    def _constrain_date(self):
        for employee in self:
            if (
                employee.date_start,
                employee.date_end,
                employee.date_start > employee.date_end,
            ):
                raise ValidationError(
                    _("The entry date must be before obsolescence date")
                )

    @api.constrains("mutual_insurance_date_start", "mutual_insurance_date_end")
    def _constrain_mutual_insurance_date(self):
        for employee in self:
            if (
                employee.mutual_insurance_date_start,
                employee.mutual_insurance_date_end,
                employee.mutual_insurance_date_start
                > employee.mutual_insurance_date_end,
            ):
                raise ValidationError(
                    _("The start date of mutual insurance must be before the end date")
                )

    @api.constrains(
        "contribution_exemption_date_start", "contribution_exemption_date_end"
    )
    def _constrain_exemption_date(self):
        for employee in self:
            if (
                employee.contribution_exemption_date_start,
                employee.contribution_exemption_date_end,
                employee.contribution_exemption_date_start
                > employee.contribution_exemption_date_end,
            ):
                raise ValidationError(
                    _("The start date of exemption must be before the end date")
                )
