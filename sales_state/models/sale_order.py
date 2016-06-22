# -*- coding: utf-8 -*-

from openerp import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('valorar', "Pendiente valorar"),('valorado', "Valorado")])
    #state = fields.Selection(selection_add=[('valorar', "Para valorar"),('valorado', "Valorado")])

#    @api.one
#    def action_quotation_approve(self):
#        self.state = 'quotation_approved'

    @api.multi
    def action_quotation_valorar(self):   	
        self.write({'state': 'valorar'})

    @api.multi
    def action_quotation_valorado(self):   	
        self.write({'state': 'valorado'})


 #   @api.multi
 #   def action_quotation_valorado(self):   	
 #       self.write({'state': 'valorado'})

        