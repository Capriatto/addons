# -*- coding: utf-8 -*-

from openerp import models, fields, api

class SaleQuotation(models.Model):
    _name = 'sale.quotation'

    h_estimadas = fields.Float(string="Horas estimadas", readonly=True, states={'draft': [('readonly', False)]}, help="Establece el número de horas estimadas para la fabricación del pedido")
    coste_hora = fields.Float(string="Coste por hora", readonly=True, states={'draft': [('readonly', False)]}, help="Valoración de la hora de trabajo en €/h")
    valoracion = fields.Float(compute="_get_total", string="Total valoración", readonly=True)

    @api.one
    @api.depends(
        'h_estimadas',
        'coste_hora',
    )
    def _get_total(self):
        total = self.h_estimadas * self.coste_hora
        self.valoracion = total
   
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    h_estimadas = fields.Float(string="Horas estimadas", readonly=True, states={'draft': [('readonly', False)]}, help="Establece el número de horas estimadas para la fabricación del pedido")
    coste_hora = fields.Float(string="Coste por hora", readonly=True, states={'draft': [('readonly', False)]}, help="Valoración de la hora de trabajo en €/h")
    valoracion = fields.Float(compute="_get_total", string="Total valoración", readonly=True)

    @api.one
    @api.depends(
        'h_estimadas',
        'coste_hora',
    )
    def _get_total(self):
        total = self.h_estimadas * self.coste_hora
        self.valoracion = total