from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class OriginStatus(models.Model):
    _name = "hr.origin.status"
    _description = "Origin Status"

    name = fields.Char()


class Certificate(models.Model):
    _name = "hr.certificate"
    _description = "Certificate Level"

    name = fields.Char()


class Role(models.Model):
    _name = "hr.coop.role"
    _description = "Role in Cooperative"

    name = fields.Char()


class SocialInsurance(models.Model):
    _name = "hr.social.insurance"
    _description = "Social Insurance"

    name = fields.Char()


class MutualInsurance(models.Model):
    _name = "hr.mutual.insurance"
    _description = "Mutual Insurance"

    name = fields.Char()


class MutualInsuranceLevel(models.Model):
    _name = "hr.mutual.insurance.level"
    _description = "Mutual Insurance Level"

    name = fields.Char()


class TransportMode(models.Model):
    _name = "hr.transport.mode"
    _description = "Transport Mode"

    name = fields.Char()


class ProfessionalLiability(models.Model):
    _name = "hr.professional.liability"
    _description = "Professional Liabilitie"

    name = fields.Char()


class Sector(models.Model):
    _name = "hr.sector"
    _description = "Sector"

    name = fields.Char()


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
    certificate = fields.Many2one(
        "hr.certificate", string="Certificate Level", required=False
    )
    bank_account_payment_id = fields.Many2one(
        "res.partner.bank",
        string="Bank Account Number for Payment",
        required=False,
        domain="[('partner_id', '=', address_home_id)]",
        help="Employee bank salary account",
    )
    coop_role_id = fields.Many2one(
        "hr.coop.role", string="Role in the cooperative", required=False
    )
    social_insurance = fields.Many2one(
        "hr.social.insurance", string="Social Insurance", required=False
    )
    mutual_insurance = fields.Many2one(
        "hr.mutual.insurance", string="Mutual Insurance", required=False
    )
    mutual_insurance_level = fields.Many2one(
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
    transport_mode = fields.Many2one(
        "hr.transport.mode", string="Transport Mode", required=False
    )
    invalidity_rate = fields.Float(
        string="Invalidity Rate", required=False, default=0
    )  # use percentage widget
    job_other_companies = fields.Text(string="Other Employers", required=False)
    job_all_hours = fields.Float(
        string="Cumulative Total Working Hours", required=False
    )  # Todo: in xml, style as 'per month'
    job_retirement = fields.Boolean(
        string="Combining Job and Retirement", required=False
    )
    job_adaptations = fields.Text(string="Job Adaptations", required=False)
    professional_liability = fields.Many2many(
        comodel_name="hr.professional.liability",
        string="Professional Liability",
        required=False,
    )
    insurance_policy = fields.Text(string="Insurance Policy", required=False)
    vehicle_insurance = fields.Text(string="Vehicle Insurance", required=False)
    office = fields.Text(string="Office", required=False)
    equipment = fields.Text(string="Equipment", required=False)
    sector = fields.Many2many(comodel_name="hr.sector", string="Sector", required=False)
    adult_dependents = fields.Integer(string="Adult Dependents", required=False)
    social_worker = fields.Text(string="Social Worker", required=False)
    contribution_date_start = fields.Date(
        string="Start Date of Contributions", required=False
    )
    # contribution_arrangements = fields.Selection(
    #     related="partner_id.contribution_arrangements"
    # )
    exemptions_contribution_reason = fields.Text(
        string="Reason for Exemption", required=False
    )
    exemption_contribution_date_start = fields.Date(
        string="Start Date of Exemption", required=False
    )
    exemption_contribution_end_start = fields.Date(
        string="End Date of Exemption", required=False
    )

    _sql_constraints = [
        (
            "check_invalidity_rate",
            "CHECK(invalidity_rate >= 0 AND invalidity_rate <= 100)",
            "The percentage of an invalidity_rate should be between 0 and 100.",
        ),
        (
            "check_job_all_hours",
            "CHECK(job_all_hours >= 0)",
            "The cumulative total working hours should greater then or equal to 0.",
        ),
        (
            "check_adult_dependents",
            "CHECK(adult_dependents >= 0)",
            "The number of Adult Dependents should greater then or equal to 0.",
        ),
    ]

    @api.constrains(
        "exemption_contribution_date_start", "exemption_contribution_date_end"
    )
    def _constrain_exemption_date(self):
        for employee in self:
            if (
                employee.exemption_contribution_date_start,
                employee.exemption_contribution_date_end,
                employee.exemption_contribution_date_start
                > employee.exemption_contribution_date_end,
            ):
                raise ValidationError(
                    _("The start date of exemption must be before the end date")
                )

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
