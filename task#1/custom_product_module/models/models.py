from odoo import fields, models, api, exceptions


class Product(models.Model):
    _inherit = 'product.template'

    tracking = fields.Selection([('unique', 'By Unique Serial Number'), ('lots', 'By Lots'), ('not', 'No tracking')],
                                string='Tracking', default='not')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def _check_product(self):
        for item in self.order_line:
            product_name = item.name
            product_qty = item.product_uom_qty
            if item.product_id.tracking == 'unique' and product_qty > 1:
                raise exceptions.ValidationError(
                    '{} marked as "unique" it\'s impossible to add more than one item'.format(product_name))


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('order_line')
    def _check_product(self):
        for item in self.order_line:
            product_name = item.name
            product_qty = item.product_qty
            if item.product_id.tracking == 'unique' and product_qty > 1:
                raise exceptions.ValidationError(
                    '{} marked as "unique" it\'s impossible to add more than one item'.format(product_name))
