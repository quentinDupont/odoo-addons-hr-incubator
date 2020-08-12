# Copyright 2019 Coop IT Easy SCRL fs
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "HR CAE Promotion",
    "summary": "Manage promotions in a CAE.",
    "author": "Coop IT Easy SCRLfs",
    "website": "https://www.coopiteasy.be",
    "category": "Human Resources",
    "version": "12.0.1.2.0",
    "license": "AGPL-3",
    "depends": ["hr_cae", "hr_cae_contract_recruitment"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_applicant.xml",
        "views/hr_employee.xml",
        "views/hr_promotion.xml",
    ],
    "demo": ["demo/demo.xml"],
    "installable": True,
    "application": False,
}
