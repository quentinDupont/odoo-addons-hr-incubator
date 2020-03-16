# Copyright 2020 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class Event(models.Model):
    _inherit = "event.event"

    show_button_create_user_for_all_participants = fields.Boolean(
        string="Show Button Create User For All Participants",
        compute="_compute_show_button_create_user_for_all_participants",
    )

    @api.multi
    @api.depends("seats_expected")
    def _compute_show_button_create_user_for_all_participants(self):
        for event in self:
            event.show_button_create_user_for_all_participants = (
                event.seats_expected != 0
            ) and (
                event.event_type_id
                == self.env.ref(
                    "coopaname_custom.event_type_accounting_workshop"
                )
            )

    def button_create_user_for_all_participants(self):
        self.ensure_one()
        for registration in self.registration_ids:
            if (
                registration.employee_id
                and registration.employee_id.work_email
            ):
                registration.employee_id.create_user_expense_report_access()
            if registration.partner_id and registration.partner_id.email:
                registration.partner_id.create_user_expense_report_access()
