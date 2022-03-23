{
    'name': 'Real Estate',
    'version': '1.0',
    'description': 'A test module for learning',
    'summary': 'Testing odoo',
    'author': 'Jaynil',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'demo/demo.xml',
        'security/ir.model.access.csv',
        'views/estate_users_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_wizards.xml',
        'views/estate_menu_views.xml',
        'reports/estate_report_views.xml',
        'reports/estate_views.xml'
    ],
    'application': True,
}
