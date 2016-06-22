# -*- coding: utf-8 -*-

from openerp import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('valorado', "Valorado")])

    @api.multi
    def action_quotation_valorado(self):   	
        self.write({'state': 'valorado'})
