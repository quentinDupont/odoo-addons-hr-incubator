from odoo import api, models


class CreateUserPortalAccessFromPartner(models.TransientModel):
    _name = "create.user.portal.access.from.partner.wizard"
    _description = "Create User with Portal Acces from Partner"

    @api.multi
    def create_user_portal_access(self):
        self.ensure_one()
        selected_partners = self.env["res.partner"].browse(
            self._context.get("active_ids")
        )
        selected_partners.create_user_portal_access()
        return True


class CreateUserPortalAccessFromEmployee(models.TransientModel):
    _name = "create.user.portal.access.from.employee.wizard"
    _description = "Create User with Portal Acces from Employee"

    @api.multi
    def create_user_portal_access(self):
        self.ensure_one()
        selected_employees = self.env["hr.employee"].browse(
            self._context.get("active_ids")
        )
        selected_employees.create_user_portal_access()
        return True
