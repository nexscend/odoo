# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Product Category Management',
    'version' : '0.1',
    'sequence': 185,
    'category': 'product',
    'website' : 'https://www.nexscend.com',
    'summary' : 'Manage your Product Category',
    'description' : """
Inventory, warehouse, sale, purchase
==================================
'Manage your Inventory with Multiple Warehouse'
""",
    'depends': [
        'base',
        'mail',
        'product',
    ],
    'data': [
        'security/raw_matrial_security.xml',
        'security/ir.model.access.csv',
        'views/fleet_vehicle_model_views.xml',
    ],

    # 'demo': ['data/fleet_demo.xml'],

    'installable': True,
    'application': True,
    # 'assets': {
        # 'web.assets_backend': [
            # 'fleet/static/src/**/*',
        # ],
    # },
    'license': 'LGPL-3',
}
