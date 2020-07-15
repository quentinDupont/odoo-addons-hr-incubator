# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Job(models.Model):
    _inherit = "hr.job"

    type = fields.Selection(
        selection=[("internal", "Internal"), ("entrepreneur", "Entrepreneur")],
        string="Type",
        default="entrepreneur",
        required=True,
    )
