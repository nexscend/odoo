# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_number = fields.Char(string="Stock Number", store=True)
    case_count = fields.Char(string="Case Count", store=True)
    case_pack = fields.Char(string="Case Pack", store=True)
    case_length = fields.Char(string="Case Length", store=True)
    case_height = fields.Char(string="Case Height", store=True)
    case_cube = fields.Char(string="Case Cube(ft3)", store=True)
    case_weight = fields.Char(string="Case weight(lbs)", store=True)
    case_width = fields.Char(string="Case Width", store=True)
    upc = fields.Char(string="UPC",)
    mil = fields.Char(string="Mil",)
    zipper_type = fields.Char(string="Type",)

    is_paper_bag = fields.Boolean('Is Paper Bags', store=True, related="categ_id.is_paper_bag")
    is_tshirt_bag = fields.Boolean('Is T-Shirt Bags', store=True, related="categ_id.is_tshirt_bag")
    is_go_green_bag = fields.Boolean('Is Go Green Bags', store=True, related="categ_id.is_go_green_bag")
    is_garbage_bag = fields.Boolean('Is Garbage Bags', store=True, related="categ_id.is_garbage_bag")
    is_ice_bag = fields.Boolean('Is Ice Bags Bags', store=True, related="categ_id.is_ice_bag")
    is_produce_bag = fields.Boolean('Is Produce Bags Bags', store=True, related="categ_id.is_produce_bag")
    is_reuse_bag = fields.Boolean('Is Reuse Bags Bags', store=True, related="categ_id.is_reuse_bag")
    is_wrap_bag = fields.Boolean('Is Stretch Wrap - Pallet Wrap Bags', store=True, related="categ_id.is_wrap_bag")
    is_zipper_bag = fields.Boolean('Is Zipper Bags Bags', store=True, related="categ_id.is_zipper_bag")


class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_paper_bag = fields.Boolean('Is Paper Bags', store=True)
    is_tshirt_bag = fields.Boolean('Is T-Shirt Bags', store=True)
    is_go_green_bag = fields.Boolean('Is Go Green Bags', store=True)
    is_garbage_bag = fields.Boolean('Is Garbage Bags', store=True)
    is_ice_bag = fields.Boolean('Is Ice Bags Bags', store=True)
    is_produce_bag = fields.Boolean('Is Produce Bags Bags', store=True)
    is_reuse_bag = fields.Boolean('Is Reuse Bags Bags', store=True)
    is_wrap_bag = fields.Boolean('Is Stretch Wrap - Pallet Wrap Bags', store=True)
    is_zipper_bag = fields.Boolean('Is Zipper Bags Bags', store=True)