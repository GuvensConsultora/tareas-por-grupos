# -*- coding: utf-8 -*-
{
    'name': "geotek",

    'summary': "Creación de tares para asociarles los productos",

    'description': """
Seleccionamos las diferentes lineas en los pptos de ventas mediante grupos para que las tareas se generen por grupos y no por productos.
    """,

    'author': "Guvens",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '18.0',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

