# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
   
    product_length = fields.Float(
        related="product_variant_ids.product_length", readonly=False
    )
    product_height = fields.Float(
        related="product_variant_ids.product_height", readonly=False
    )
    product_width = fields.Float(
        related="product_variant_ids.product_width", readonly=False
    )
    volume = fields.Float(
        compute="_compute_volume",
        readonly=False,
        store=True,
    )

    @api.model
    def _calc_volume(self, product_length, product_height, product_width):
        volume = 0
        if product_length and product_height and product_width:
            length_m = self.convert_to_meters(product_length)
            height_m = self.convert_to_meters(product_height)
            width_m = self.convert_to_meters(product_width)
            volume = length_m * height_m * width_m

        return volume

    @api.depends(
        "product_length", "product_height", "product_width"
    )
    def _compute_volume(self):
        for template in self:
            template.volume = template._calc_volume(
                template.product_length,
                template.product_height,
                template.product_width,
            )

    def convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env.ref("uom.product_uom_meter")

        return dimensional_uom._compute_quantity(
            qty=measure,
            to_unit=uom_meters,
            round=False,
        )

    def _prepare_variant_values(self, combination):
        """
        As variant is created inside template create() method and as
        template fields values are flushed after _create_variant_ids(),
        we catch the variant values preparation to update them
        """
        res = super()._prepare_variant_values(combination)
        if self.product_length:
            res.update({"product_length": self.product_length})
        if self.product_height:
            res.update({"product_height": self.product_height})
        if self.product_width:
            res.update({"product_width": self.product_width})
        return res
