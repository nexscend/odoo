# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Sale Sourced by Line",
    "summary": "Multiple warehouse source locations for Sale order",
    "version": "17.0.1.0.0",
    "category": "Warehouse",
    'sequence': 200,
    "author": "brain-tec AG, ADHOC SA, Camptocamp SA, ",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/sale-workflow",
    "depends": [
        "sale_procurement_group_by_line",
    ],
    "data": [
        'security/ir.model.access.csv',
        "view/sale_view.xml",
        "view/sale_view_line_wizard.xml",
        ],
    # "data": [],
    "installable": True,
    'application': True,
}
