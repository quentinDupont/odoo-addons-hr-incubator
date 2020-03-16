# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    users_count = fields.Integer(
        string="Users Count", compute="_compute_users_count"
    )

    @api.multi
    @api.depends("email")
    def _compute_users_count(self):
        for partner in self:
            partner.users_count = len(
                self.env["res.users"].search([("login", "=", partner.email)])
            )

    @api.multi
    def create_user_expense_report_access(self):
        group_id = self.env.ref("hr_expense.group_hr_expense_user").id
        company_id = (
            self.env["res.company"]._company_default_get("res.users").id
        )

        for partner in self:
            if not partner.email:
                raise ValidationError(_("An email address is required."))
            user = self.env["res.users"].search(
                [("login", "=", partner.email)], limit=1
            )
            if user:
                user.write({"active": True, "groups_id": [(4, group_id)]})
            else:
                user_values = {
                    "partner_id": partner.id,
                    "email": partner.email,
                    "login": partner.email,
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
