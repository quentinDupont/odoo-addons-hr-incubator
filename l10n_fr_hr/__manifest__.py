# Copyright 2020 GRAO
#   Quentin DUPONT <https://twitter.com/pondupont>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'French Localization for HR',
    'summary': 'French Localization for HR',
    'version': '12.0.1.0.0',
    'category': 'French Localization',
    'author': 'GRAP,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': [
        'hr_cae',
        'l10n_fr_department',
    ],
    "data": [
        "views/hr_employee.xml",
    ],
    'installable': True,
    'auto_install': True,
}
