# Copyright 2020 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def create_user_expense_report_access(self):
        group_id = self.env.ref("hr_expense.group_hr_expense_user").id
        company_id = (
            self.env["res.company"]._company_default_get("res.users").id
        )

        for partner in self:
            user = self.env["res.users"].search(
                [("login", "=", partner.email)]
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
                    .with_context(no_reset_password=True)
                    ._create_user_from_template(user_values)
                )

                (
                    user.sudo()
                    .with_context({"create_user": True, "active_test": True})
                    .action_reset_password()
                )
