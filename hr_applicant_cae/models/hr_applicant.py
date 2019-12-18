from odoo import fields, models


class Applicant(models.Model):
    _inherit = "hr.applicant"

    country_of_birth = fields.Many2one("res.country", string="Country of Birth")
