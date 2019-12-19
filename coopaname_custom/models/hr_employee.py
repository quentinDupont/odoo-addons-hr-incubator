# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


import logging

from odoo import _, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _inherit = "hr.employee"

    _sql_constraints = [
        (
            "identification_id_uniq",
            "unique(identification_id)",
            _(
                "The Employee Identification Number must "
                "be unique across the company(s)."
            ),
        )
    ]

    @api.model
    def _generate_identification_id(self, firstname, lastname):
        try:
            assert firstname
            assert lastname
        except AssertionError:
            raise ValidationError(
                _(
                    "First name and last name are required to generate "
                    "Identification No "
                )
            )

        firstname_initial = firstname[0]
        if len(lastname.split()) > 1:
            lastnames = lastname.split()
            lastname_initials = lastnames[0][0] + lastnames[1][0]
        else:
            lastname_initials = lastname[0]

        initials = (firstname_initial + lastname_initials).upper()
        seq_number = self.env["ir.sequence"].next_by_code(
            "hr.employee.identification_id"
        )
        return "{}{}".format(initials, seq_number)

    @api.model
    def create(self, values):
        employee = super().create(values)
        if not employee.identification_id:
            employee.identification_id = self._generate_identification_id(
                employee.firstname, employee.lastname
            )
        return employee
