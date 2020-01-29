# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
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

    def test_generate_employee_identification_id_from_name(self):
        employee_obj = self.env["hr.employee"]
        sequence_next = int(
            self.env.ref("coopaname_custom.seq_employee_identification_id").next_by_id()
        )

        ernest_id = employee_obj.create(
            {"firstname": "Ernest", "lastname": "Lapalisse"}
        ).identification_id
        self.assertEquals(ernest_id, "EL%s" % (sequence_next + 1))

        sylvaindutilleul_id = employee_obj.create(
            {"firstname": "Sylvain", "lastname": "Du Tilleul"}
        ).identification_id
        self.assertEquals(sylvaindutilleul_id, "SDT%s" % (sequence_next + 2))

        sylvaindutilleul_id = employee_obj.create(
            {"firstname": "Philippe", "lastname": "De Saxe Cobourg Gotta"}
        ).identification_id
        self.assertEquals(sylvaindutilleul_id, "PDS%s" % (sequence_next + 3))

        with self.assertRaises(ValidationError):
            employee_obj.create({"lastname": "lastname"})

        with self.assertRaises(ValidationError):
            employee_obj.create({"firstname": "firstname"})

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
