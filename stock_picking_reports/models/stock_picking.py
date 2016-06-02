# -*- coding: utf-8 -*-

from openerp import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    deliver = fields.Char(string="Deliver at")
