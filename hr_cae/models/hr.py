from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    department_id = fields.Many2one("res.country.department", string="Department")
    nationality_ids = fields.Many2many("res.country", string="Nationalities")
    country_birth_id = fields.Many2one("res.country", string="Country of Birth")
    date_start = fields.Date(string="Date of start", default=fields.Date.today())
    date_end = fields.Date()
