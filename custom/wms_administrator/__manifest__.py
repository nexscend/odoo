# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'WMS Administrator',
    'version' : '0.1',
    'sequence': 185,
    'category': 'Inventory',
    'website' : 'https://www.nexscend.com',
    'summary' : 'Manage your opeartion of Administrator',
    'description' : """
Inventory, warehouse, sale, purchase
""",
    'depends': [
        'nex_product_cate_raw_material',
        'product_dimension',
    ],
    'data': [
        'views/administrator_view.xml',
    ],


    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
