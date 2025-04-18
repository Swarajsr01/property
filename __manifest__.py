# -*- coding: utf-8 -*-

{
    'name': "Property",
    'version': '1.0',
    'depends': ['base', 'mail', 'contacts', 'account', 'hr'],
    'author': "STARLIN",
    'category': 'All',
    'description': """
    Property Management
    """,
    'data': [
        'security/property_groups.xml',
        'security/property_security.xml',
        'security/ir.model.access.csv',

        'data/rent_management_sequence.xml',
        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',
        'data/paper_format_demo.xml',
        'data/website_menu.xml',

        'report/rent_lease_report_wizard_template.xml',
        'report/rent_lease_report_wizard_reports.xml',

        'wizard/rent_lease_report_wizard_views.xml',

        'views/property_management_views.xml',
        'views/rent_management_views.xml',
        'views/property_facilities_views.xml',
        'views/res_partner_views.xml',
        'views/properties_website_template.xml',
        'views/property_menuitems.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'property/static/src/js/action_manager.js',
        ],
    },
    'assets': {
        'web.assets_frontend': [
            'web/static/src/legacy/js/public/public_widget.js',
            'property/static/src/js/inline_sum.js',
        ],
    },
}
