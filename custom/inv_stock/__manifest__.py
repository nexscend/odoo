# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Inventory Management',
    'version' : '0.1',
    'sequence': 185,
    'category': 'Inventory',
    'website' : 'https://www.nexscend.com',
    'summary' : 'Manage your Inventory with Multiple Warehouse',
    'description' : """
Inventory, warehouse, sale, purchase
==================================
'Manage your Inventory with Multiple Warehouse'
""",
    'depends': [
        'mail',
        'contacts',
        'uom',
        'product',
        'delivery',
        'sale_management',
        'sale_purchase',
        'sale_stock',
        'stock_account',
        'stock_sms',
        'stock_delivery',
        'stock_dropshipping',
        'nex_product_cate_raw_material',
    ],
    'data': [
        'views/menu_raw_material.xml',
    ],

   'installable': True,
    'application': True,
    # 'assets': {
        # 'web.assets_backend': [
            # 'fleet/static/src/**/*',
        # ],
    # },
    'license': 'LGPL-3',
}
