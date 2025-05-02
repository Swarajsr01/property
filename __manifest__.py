# -*- coding: utf-8 -*-

{
    'name': "Property",
    'version': '1.0',
    'depends': ['base', 'mail', 'contacts', 'account', 'hr','website','product','point_of_sale'],
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

        'views/product_template_views.xml',

        'views/rent_website_template.xml',
        'views/thank_you_page.xml',
        'views/portal_template.xml',
        'views/snippets/properties_template.xml',
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
        'web.assets_frontend': [
            'property/static/src/js/website_rent_order.js',
            'property/static/src/xml/properties_snippet_template.xml',
            'property/static/src/js/properties_snippet.js',
        ],
        'point_of_sale._assets_pos': [
            'property/static/src/xml/pos_product_rating.xml',# test
            'property/static/src/js/product_card_rating.js',# test
            'property/static/src/js/orderline_receipt.js',# test
            # 'property/static/src/js/test.js',# test
        ],
        # 'point_of_sale.assets': [
        #     'property/static/src/js/test.js',# test
        #     'property/static/src/xml/extra_fieldss.xml',# test
        # ],
    },
}
