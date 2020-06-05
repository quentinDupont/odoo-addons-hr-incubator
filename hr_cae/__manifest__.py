# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "HR CAE",
    "summary": "Manage employee HR in a CAE.",
    "author": "Coop IT Easy SCRLfs",
    "website": "https://www.coopiteasy.be",
    "category": "Human Resources",
    "version": "12.0.1.2.0",
    "license": "AGPL-3",
    "depends": ["hr", "hr_employee_age"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr.xml",
        "views/hr_employee.xml",
        "data/data.xml",
    ],
    "installable": True,
    "application": False,
}
