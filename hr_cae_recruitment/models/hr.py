# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class OriginStatus(models.Model):
    _name = "hr.origin.status"
    _description = "Origin Status"

    name = fields.Char()


class OriginStatusDetails(models.Model):
    _name = "hr.origin.status.details"
    _description = "Origin Status Details"

    name = fields.Char()
    origin_status_id = fields.Many2one(
        comodel_name="hr.origin.status", string="Origin Status", required=False
    )
