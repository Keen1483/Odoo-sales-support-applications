# -*- coding: utf-8 -*-
{
    'name': "rapport_pb_journalier",

    'summary': """
        Rapport des BP
        """,

    'description': """
        Rapport des BP
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'caisse_depense', 'hr_expense', 'first_module_new', 'report_xlsx'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/report_def.xml',
        'report/template_bp.xml',
        'views/bp_journalier_views.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
