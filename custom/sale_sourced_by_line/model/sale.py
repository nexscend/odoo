# Copyright 2013-2014 Camptocamp SA - Guewen Baconnier
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
_logger = logging.getLogger(__name__)



class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    # @api.model
    # def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
    #     if 'only_product_related_warehouse_show' in self.env.context:
    #         return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)
    #     return super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, order=None):
       # code
        domain = []
        warehouse_data = []
        if 'only_product_related_warehouse_show' in self.env.context:
            order_line_id = self.env.context.get('only_product_related_warehouse_show')
            product_id = self.env['sale.order.line'].browse(order_line_id).product_id
            warehouse_ids = self.search([('id', '!=', False)])
            for warehouse_id in warehouse_ids:
                total_qty = self.env['stock.quant']._get_available_quantity(product_id, warehouse_id.lot_stock_id) if product_id else 0.0
                if total_qty > 0:
                    warehouse_data.append(warehouse_id.id)
                domain = expression.AND([domain, [('id', 'in', warehouse_data)]])
        return self._search(expression.AND([domain, args]), limit=limit,   access_rights_uid=name_get_uid)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Default Warehouse",
        readonly=True,
        help="If no source warehouse is selected on line, "
        "this warehouse is used as default. ",
    )


class StockWarehouseLine(models.Model):
    _name = "stock.warehouse.line"
    _description = "Stock Warehouse Line"


    name = fields.Char('Name', translate=True)
    sequence = fields.Integer(default=10)
    order_line_id = fields.Many2one(
        "sale.order.line",
        string="Order Line",
        related="wizard_id.order_line_id"
    )
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        "Warehouse",
    )

    wizard_id = fields.Many2one(
        "sale.order.line.wizard",
        "Warehouse",
    )

    available_quantity = fields.Float(
        'Available Quantity',
        help="On hand quantity which hasn't been reserved on a transfer, in the default unit of measure of the product",
        digits='Product Unit of Measure')

    
    qty_delivered = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure')

    @api.onchange('order_line_id')
    def onchange_order_line_id(self):
        res = {}
        product_warehouse_ids = []
        all_warehouse_ids = self.env['stock.warehouse'].search([('id', '!=', False)])
        for warehouse_id in all_warehouse_ids:
            total_qty = self.env['stock.quant']._get_available_quantity(self.order_line_id.product_id, warehouse_id.lot_stock_id) if self.order_line_id.product_id else 0.0
            if total_qty != 0:
                product_warehouse_ids.append(warehouse_id.id)
        res['domain'] = {'warehouse_id': [('id', 'in', product_warehouse_ids)]}
        return res

    @api.onchange('qty_delivered')
    def _on_change_qty_delivereds(self):
        if self.qty_delivered and self.qty_delivered > self.available_quantity :
            raise ValidationError(_("Quantity not More then %s Available Quantity", self.available_quantity))

    @api.onchange('warehouse_id')
    def _on_change_warehouse_id(self):
        for rec in self: 
            rec.available_quantity = self.env['stock.quant']._get_available_quantity(rec.order_line_id.product_id, rec.warehouse_id.lot_stock_id) if rec.order_line_id.product_id else 0.0



class SaleOrderLineWizard(models.Model):
    _name = "sale.order.line.wizard"
    _description = "Sale Order Line Wizard"

    order_line_id = fields.Many2one(
        "sale.order.line",
        string="Order Line"
    )
    product_warehouse_ids = fields.One2many(
        "stock.warehouse.line",
        "wizard_id",
        "Warehouse",
    )
    product_id = fields.Many2one('product.product', string='Product')
    qty_delivered = fields.Float(
        string="Delivery Quantity",
        digits='Product Unit of Measure')


    @api.onchange('product_warehouse_ids')
    def _on_change_product_warehouse_ids(self):
        if self.product_warehouse_ids and sum(self.product_warehouse_ids.mapped('qty_delivered')) > self.qty_delivered :
            raise ValidationError(_("Quantity not More then %s", self.qty_delivered))


    def change_product_qty(self):
        _logger.info("Update Details...")

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    def action_create_so_line_warehouse(self):
        self.ensure_one()
        return {
            'name': _('Warehouse Quantity'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sale.order.line.wizard',
            'target': 'new',
            'context': {
                'default_order_line_id': self.id,
                'default_product_id': self.product_id.id,
                'default_qty_delivered': self.product_uom_qty,
                'default_product_warehouse_ids':  [(6, 0, self.env['stock.warehouse.line'].search([('order_line_id', '=', self.id)]).ids)],
            },

        }


    warehouse_id = fields.Many2one(
        "stock.warehouse",
        "Warehouse",
        related="",
        help="If a source warehouse is selected, "
        "it will be used to define the route. "
        "Otherwise, it will get the warehouse of "
        "the sale order",
    )

    product_warehouse_ids = fields.One2many(
        "stock.warehouse.line",
        "order_line_id",
        "Warehouse",
    )


    def _prepare_procurement_group_vals(self):
        vals = super(SaleOrderLine, self)._prepare_procurement_group_vals()
        # for compatibility with sale_quotation_sourcing
        if self._get_procurement_group_key()[0] == 10:
            if self.product_warehouse_ids:
                vals["name"] += ' '.join(self.product_warehouse_ids.mapped('warehouse_id').mapped('name'))
        return vals

    def _prepare_procurement_values(self, group_id=False, warehouse_id=False):
        """Prepare specific key for moves or other components
        that will be created from a stock rule
        comming from a sale order line. This method could be
        override in order to add other custom key that could
        be used in move/po creation.
        """
        values = super(
            SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        if warehouse_id != False and warehouse_id != None:
            values["warehouse_id"] = warehouse_id
        return values

    def _get_procurement_group_key(self):
        """Return a key with priority to be used to regroup lines in multiple
        procurement groups

        """
        priority = 10
        key = super(SaleOrderLine, self)._get_procurement_group_key()
        # Check priority
        if key[0] >= priority:
            return key
        wh_id = (
            self.warehouse_id.id if self.warehouse_id else self.order_id.warehouse_id.id
        )
        return priority, wh_id
