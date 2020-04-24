# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "HR CAE",
    "summary": "Employee HR in a CAE - Cooperative Activité Emploi",
    "author": "Coop IT Easy SCRL",
    "website": "https://coopiteasy.be",
    "category": "Human Resources",
    "version": "12.0.1.0.1",
    "license": "AGPL-3",
    "depends": ["hr", "hr_employee_age"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr.xml",
        "views/hr_employee.xml",
        "views/hr_exemption.xml",
        "data/data.xml",
    ],
    "installable": True,
    "application": False,
}
