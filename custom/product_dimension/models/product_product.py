# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models




class ProductDimension(models.Model):
    _name = "product.dimension"
    _description = "product.dimension"

    name = fields.Char("Name")
    product_length = fields.Float("Length")
    product_height = fields.Float("Height")
    product_width = fields.Float("Width")
    category_id = fields.Many2one('product.category', 'Category')
    product_id = fields.Many2one('product.product', 'Product')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.category_id = self.product_id.categ_id.id


class ProductCategory(models.Model):
    _inherit = "product.category"

    dimension_ids = fields.One2many('product.dimension', 'category_id', 'Dimension')

class ProductProduct(models.Model):
    _inherit = "product.product"

    product_length = fields.Float("Length")
    product_height = fields.Float("Height")
    product_width = fields.Float("Width")
 
    volume = fields.Float(
        compute="_compute_volume",
        readonly=False,
        store=True,
    )

    @api.depends(
        "product_length", "product_height", "product_width"
    )
    def _compute_volume(self):
        template_obj = self.env["product.template"]
        for product in self:
            product.volume = template_obj._calc_volume(
                product.product_length,
                product.product_height,
                product.product_width,
            )
