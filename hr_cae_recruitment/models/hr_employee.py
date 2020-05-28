# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    # TODO: check that this one is actually used in logic
    turnover_minimum = fields.Monetary(string="Minimum Turn-Over")
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
        "hr.recruitment.degree", string="Certificate", required=False
    )
    certificate_date = fields.Date(
        string="Certificate Date",
        help="Certificate Delivery Date",
        required=False,
    )
    professional_experience = fields.Text(
        string="Professional Experience", required=False
    )
