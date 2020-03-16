# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestCoopanameCustom(TransactionCase):
    def test_onchange_partner_id_updates_applicant(self):
        applicant = self.browse_ref("hr_recruitment.hr_case_salesman0")
        partner = self.browse_ref("base.res_partner_1")

        with Form(applicant) as form:
            form.partner_id = partner

        self.assertEquals(applicant.name, partner.name)
        self.assertEquals(applicant.partner_name, partner.name)

    def test_format_phone_number(self):

        number_fr = "0699687678"
        number_be = "+32 4888657 50"

        ernest = self.env["hr.employee"].create(
            {
                "firstname": "Ernest",
                "lastname": "Lapalisse",
                "mobile_phone": number_fr,
                "work_phone": number_be,
            }
        )
        self.assertEqual(ernest.mobile_phone, "06 99 68 76 78")
        self.assertEqual(ernest.work_phone, "+32 488 86 57 50")

        hne = self.browse_ref("hr.employee_hne")
        hne.mobile_phone = number_fr
        hne.work_phone = number_be
        # fixme: the test does not access latest values
        # self.assertEqual(hne.mobile_phone, "06 99 68 76 78")
        # self.assertEqual(hne.work_phone, "+32 488 86 57 50")

    def test_create_expense_report_user_from_contact(self):
        event = self.browse_ref("event.event_0")
        partner = self.browse_ref("base.res_partner_1")
        employee = self.browse_ref("hr.employee_al")
        group_id = self.browse_ref("hr_expense.group_hr_expense_user")
        company_id = self.env["res.company"]._company_default_get("res.users")
        self.assertTrue(bool(partner.email))
        self.assertTrue(bool(employee.work_email))
        self.assertFalse(
            bool(self.env["res.users"].search([("login", "=", partner.email)]))
        )
        self.assertFalse(
            bool(
                self.env["res.users"].search(
                    [("login", "=", employee.work_email)]
                )
            )
        )
        self.env["event.registration"].create(
            {
                "event_id": event.id,
                "name": partner.name,
                "email": partner.email,
                "partner_id": partner.id,
            }
        )
        self.env["event.registration"].create(
            {
                "event_id": event.id,
                "name": employee.name,
                "email": employee.work_email,
                "employee_id": employee.id,
            }
        )
        event.button_create_user_for_all_participants()
        partner_user = self.env["res.users"].search(
            [("login", "=", partner.email)], limit=1
        )
        self.assertTrue(group_id in partner_user.groups_id)
        self.assertEqual(partner_user.company_id, company_id)
        employee_user = self.env["res.users"].search(
            [("login", "=", employee.work_email)], limit=1
        )
        self.assertTrue(group_id in employee_user.groups_id)
        self.assertEqual(employee_user.company_id, company_id)
