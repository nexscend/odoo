# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProductCategoryRawMaterial(models.Model):
    _name = "product.category.raw.material"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Product Category Raw Material"
    _order = "create_date desc"

    name = fields.Char(string="Name")
    price = fields.Float(string='Raw Material Cost', tracking=True)


class Product_Category(models.Model):
    _inherit = 'product.category'
    
    raw_material_id = fields.Many2one(
        'product.category.raw.material', 'Raw Material',
    )

    