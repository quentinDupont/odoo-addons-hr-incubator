# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Coopaname Custom",
    "summary": """
        Customization specific to Coopaname use case.
    """,
    "license": "AGPL-3",
    "author": "Coop IT Easy SCRLfs",
    "website": "https://www.coopiteasy.be",
    "category": "Human Resources",
    "version": "12.0.0.2.0",
    "depends": [
        "base_location_geonames_import",
        "contacts",
        "hr_cae",
        "hr_cae_contract",
        "hr_cae_documents",
        "hr_cae_event",
        "hr_cae_event_promotion",
        "hr_cae_promotion",
        "hr_employee_firstname",
        "hr_expense",
        "hr_recruitment",
        "member_data_history",
        "l10n_fr",
    ],
    "data": [
        "wizard/create_user_portal_access.xml",
        "data/data.xml",
        "views/event.xml",
        "views/hr_applicant.xml",
        "views/hr_employee.xml",
        "views/res_partner.xml",
    ],
    "demo": [],
    "external_dependencies": {"python": ["phonenumbers"]},
    "installable": True,
}
