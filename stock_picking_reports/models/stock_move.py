# -*- coding: utf-8 -*-
from openerp import fields, models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    sale_price_unit = fields.Float(
        string="Sale price unit", readonly=True,
        related='procurement_id.sale_line_id.price_unit')
    sale_discount = fields.Float(
        string="Sale discount (%)", readonly=True,
        related='procurement_id.sale_line_id.discount')
    sale_price = fields.Float(
        string="Sale price", readonly=True,
        compute='_get_sale_price')

    @api.one
    @api.depends(
        'sale_price_unit',
        'sale_discount',
        'product_qty',
        'procurement_id.sale_line_id.order_id.currency_id',
    )
    def _get_sale_price(self):
        sale_price_tot = (self.sale_price_unit *
                    (1 - (self.sale_discount or 0.0) / 100.0))
        # Only get sale_price_tot if this stock.move belongs to a
        # stock.picking created from a sale.order
        if self.procurement_id and self.procurement_id.sale_line_id:
            # Round by currency precision
            currency = self.procurement_id.sale_line_id.order_id.currency_id
            if currency:
                sale_price_tot = currency.round(sale_price_tot)
        # Write sale_price_tot into record (cache because this field is store=False)
        self.sale_price = sale_price_tot
