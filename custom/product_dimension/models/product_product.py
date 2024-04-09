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
    product_temp_id = fields.Many2one('product.template', 'Product')
    attribute_id = fields.Many2one('product.attribute', 'Attribute')
    is_product_dimension = fields.Boolean('Is Product dimension', related="attribute_id.is_product_attribute")

    @api.onchange(
        'attribute_id', 
        'product_length',
        'product_height',
        'product_width',
        )
    def onchange_product_dimension(self):
        for rec in self:
            if rec.attribute_id:
                    rec.name = False
            if rec.is_product_dimension:
                rec.name = '%s x %s x %s'%(int(rec.product_length),int(rec.product_height),int(rec.product_width))
                rec.is_product_dimension = True
            else:
                rec.is_product_dimension = False

    @api.onchange('product_temp_id')
    def _onchange_product_id(self):
        if self.product_temp_id:
            self.category_id = self.product_temp_id.categ_id.id

    @api.model_create_multi
    def create(self, vals_list):
        """Insert model_name and model_model field values upon creation."""
        res = super(ProductDimension, self).create(vals_list)
        # attribute_id = self.env['product.attribute'].search([('name', 'ilike', 'Bag Dimension')])
        record_val = {
                    'name' : res.name,
                    'attribute_id': res.attribute_id.id,
                    'dimension_id': res.id,
                    }
        product_attribute_value_id = self.env["product.attribute.value"].create(record_val)

        line_id = res.product_temp_id.attribute_line_ids.filtered(lambda line: line.attribute_id.id == res.attribute_id.id)
        if line_id:
            line_id.write({'value_ids':  [(6, 0, line_id.value_ids.ids + [product_attribute_value_id.id])]})
        else:
            self.env['product.template.attribute.line'].create({
                'product_tmpl_id' : res.product_temp_id.id,
                'attribute_id' : res.attribute_id.id,
                'value_ids' : [(6, 0, [product_attribute_value_id.id])],
                })
        return res


    def write(self, vals):
        dimension = super(ProductDimension, self).write(vals)
        attribute_id = self.env['product.attribute.value'].search([('dimension_id', '=', self.id)])
        if attribute_id:
            attribute_id.write({'name': ('%s x %s x %s'%(int(self.product_length),int(self.product_height),int(self.product_width)))})
        return dimension

class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    dimension_id = fields.Many2one('product.dimension', 'Dimension')

class ProductAttributeValue(models.Model):
    _inherit = "product.attribute"

    is_product_attribute = fields.Boolean('Is Product Attribute')


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
