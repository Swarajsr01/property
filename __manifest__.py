# -*- coding: utf-8 -*-

{
    'name': "Property",
    'version': '1.0',
    'depends': ['base', 'mail', 'contacts', 'account', 'hr','website'],
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

        'report/rent_lease_report_wizard_template.xml',
        'report/rent_lease_report_wizard_reports.xml',

        'wizard/rent_lease_report_wizard_views.xml',

        'views/website_menu.xml',
        'views/property_management_views.xml',
        'views/rent_management_views.xml',
        'views/property_facilities_views.xml',
        'views/res_partner_views.xml',
        'views/rent_website_template.xml',
        'views/thank_you_page.xml',
        'views/portal_template.xml',
        'views/category_template.xml',
        'views/property_view_template.xml',
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
            'property/static/src/js/website_rent.js',
            'property/static/src/xml/property_highlight_content.xml',
            'property/static/src/js/properties_category.js',
        ],
    },
}


# 'assets': {
#         'web.assets_frontend': [
#             '/dynamic_snippet/static/src/xml/category_highlight_content.xml',
# '/dynamic_snippet/static/src/js/product_category.js',
#         ],
#     },