# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


import logging

import phonenumbers

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


def _format_phone_number(number):
    number = phonenumbers.parse(number, "FR")
    if number.country_code == 33:
        return phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.NATIONAL
        )
    else:
        return phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )


class Employee(models.Model):
    _inherit = "hr.employee"

    users_count = fields.Integer(
        string="Users Count", compute="_compute_users_count"
    )

    @api.model
    def create(self, values):

        if "mobile_phone" in values and values["mobile_phone"]:
            values["mobile_phone"] = _format_phone_number(
                values["mobile_phone"]
            )
        if "work_phone" in values and values["work_phone"]:
            values["work_phone"] = _format_phone_number(values["work_phone"])

        employee = super().create(values)
        return employee

    @api.multi
    def write(self, values):
        if "mobile_phone" in values and values["mobile_phone"]:
            values["mobile_phone"] = _format_phone_number(
                values["mobile_phone"]
            )
        if "work_phone" in values and values["work_phone"]:
            values["work_phone"] = _format_phone_number(values["work_phone"])
        return super().write(values)

    @api.multi
    @api.depends("work_email")
    def _compute_users_count(self):
        for employee in self:
            employee.users_count = len(
                self.env["res.users"].search(
                    [("login", "=", employee.work_email)]
                )
            )

    @api.multi
    def create_user_expense_report_access(self):
        group_id = self.env.ref("hr_expense.group_hr_expense_user").id
        company_id = (
            self.env["res.company"]._company_default_get("res.users").id
        )

        for employee in self:
            if not employee.work_email:
                raise ValidationError(_("An email address is required."))
            user = self.env["res.users"].search(
                [("login", "=", employee.work_email)], limit=1
            )
            if user:
                user.write({"active": True, "groups_id": [(4, group_id)]})
            else:
                new_partner_id = self.env["res.partner"].create(
                    {
                        "is_company": False,
                        "name": employee.name,
                        "email": employee.work_email,
                    }
                )
                user_values = {
                    "partner_id": new_partner_id.id,
                    "employee_ids": [(6, 0, [employee.id])],
                    "email": employee.work_email,
                    "login": employee.work_email,
                    "groups_id": [(6, 0, [group_id])],
                    "company_id": company_id,
                    "company_ids": [(6, 0, [company_id])],
                }

                user = (
                    self.env["res.users"]
                    .sudo()
                    .with_context(no_reset_password=True)
                    ._create_user_from_template(user_values)
                )

                (
                    user.sudo()
                    .with_context({"create_user": True, "active_test": True})
                    .action_reset_password()
                )
