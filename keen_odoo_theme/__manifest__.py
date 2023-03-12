# -*- coding: utf-8 -*-
{
    'name': "keen_odoo_theme",

    'summary': """
        Customize default theme
        """,

    'description': """
        Customize default theme
    """,

    'author': "Dongmo Geraud",
    'website': "http://www.app-avenue.com.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'assets/assets.xml',
        'views/icons.xml',
        'views/layout.xml',
    ],
    "qweb": [
            'static/src/xml/sidebar.xml',
            'static/src/xml/styles.xml',
            'static/src/xml/top_bar.xml',
        ],
}
