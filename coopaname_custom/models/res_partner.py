# -*- coding: utf-8 -*-
from odoo import models, fields, api


class resPartner(models.Model):
    _inherit = "res.partner"

    initiate_date = fields.date(
        string="Date Infocoll",
        help="A quel moment, la personne fut accueillie par une information collective"
    )
