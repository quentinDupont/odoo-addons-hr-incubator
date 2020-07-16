# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestHRCAE(TransactionCase):
    def test_timesheet_sheet_add_employees(self):
        self.employee_1 = self.browse_ref("hr.employee_al")
        self.employee_2 = self.browse_ref("hr.employee_mit")
        self.account_analytic_line = self.browse_ref(
            "hr_timesheet.working_hours_coding"
        )

        self.account_analytic_line.employee_ids = [
            (6, 0, [self.employee_1.id, self.employee_2.id])
        ]
        self.assertEquals(len(self.account_analytic_line.employee_ids.ids), 2)
