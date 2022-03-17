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
        'security/ir.model.access.csv',
        'views/estate_property_offer/estate_property_offer_views.xml',
        'views/estate_property_tag/estate_property_tag_list_views.xml',
        'views/estate_property/estate_property_list_views.xml',
        'views/estate_property_tag/estate_property_tag_form_views.xml',
        'views/estate_property/estate_property_form_views.xml',
        'views/estate_property_tag/estate_property_tag_search_views.xml',
        'views/estate_property/estate_property_search_views.xml',
        'views/estate_property_tag/estate_property_tag_views.xml',
        'views/estate_property/estate_property_views.xml',
        'views/estate_property_type/estate_property_type_all_views.xml',
        'views/estate_property_type/estate_property_type_views.xml',
        'views/estate_menu_views.xml',
    ],
    'application': True,
}
