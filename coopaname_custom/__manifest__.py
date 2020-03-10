# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "coopaname_custom",
    "summary": """
        Lists all dependencies for Coopaname's deployement""",
    "license": "AGPL-3",
    "author": "Coop IT Easy SCRLfs",
    "website": "www.coopiteasy.be",
    "category": "Human Resources",
    "version": "12.0.0.1.0",
    "depends": [
        "base_location_geonames_import",
        "contacts",
        "hr_cae",
        "hr_cae_contract",
        "hr_cae_documents",
        "hr_cae_event",
        "hr_employee_firstname",
        "hr_expense",
        "hr_recruitment",
        "l10n_fr",
    ],
    "data": [
        "data/data.xml",
        "views/hr_applicant.xml",
        "views/res_partner.xml",
    ],
    "demo": [],
    "external_dependencies": {"python": ["phonenumbers"]},
    "installable": True,
}
