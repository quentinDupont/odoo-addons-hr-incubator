# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestHRCAE(TransactionCase):
    def test_create_employee_from_applicant(self):
        applicant = self.browse_ref("hr_recruitment.hr_case_salesman0")
        promotion = self.browse_ref("hr_cae_promotion.hr_promotion_test")
        self.assertEquals(promotion.no_of_places_max, 1)
        applicant.promotion_id = promotion

        self.assertTrue(applicant in promotion.applicant_ids)

        applicant.create_employee_from_applicant()
        employee = applicant.emp_id

        self.assertEquals(employee.promotion_id, applicant.promotion_id)

        self.assertTrue(employee in promotion.employee_ids)
        self.assertTrue(applicant not in promotion.applicant_ids)

    def test_promotion_no_of_places_max(self):
        promotion = self.browse_ref("hr_cae_promotion.hr_promotion_test")
        self.assertEquals(promotion.no_of_places_max, 1)

        employee_1 = self.browse_ref("hr.employee_al")
        employee_2 = self.browse_ref("hr.employee_mit")
        applicant_1 = self.browse_ref("hr_recruitment.hr_case_salesman0")

        employee_1.promotion_id = promotion

        with self.assertRaises(ValidationError):
            employee_2.promotion_id = promotion

        applicant_1.promotion_id = promotion
        self.assertFalse(applicant_1.emp_id)
        with self.assertRaises(ValidationError):
            applicant_1.create_employee_from_applicant()

        promotion.no_of_places_regime = "unlimited"
        employee_2.promotion_id = promotion

        with self.assertRaises(ValidationError):
            promotion.no_of_places_regime = "limited"
