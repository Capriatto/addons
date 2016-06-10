# -*- coding: utf-8 -*-

from openerp import models, fields, api

class CrmClaimCosts(models.Model):
    _name = 'crm.claim.costs'

    collect_mat = fields.Float(string="Collect material")
    repair_mat = fields.Float(string="Repair damaged material")
    deliver_mat = fields.Float(string="Deliver new/repaired material")
    discount = fields.Float(string="Discount")
    disc_perc = fields.Char(string="Percentage of discount")
    refund = fields.Float(string="Refund")
    other = fields.Char(string="Other")
    other_quant = fields.Float(string="Quantity")
    claim_tot = fields.Float(compute="_get_total", string="Claim total", readonly=True)

    @api.one
    @api.depends(
        'collect_mat',
        'repair_mat',
        'deliver_mat',
        'discount',
        'refund',
        'other_quant',
    )
    def _get_total(self):
        total = self.collect_mat + self.repair_mat + self.deliver_mat + self.discount + self.refund + self.other_quant
        self.claim_tot = total

class crm_claim(models.Model):
    _inherit = 'crm.claim'

    collect_mat = fields.Float(string="Collect material")
    repair_mat = fields.Float(string="Repair damaged material")
    deliver_mat = fields.Float(string="Deliver new/repaired material")
    discount = fields.Float(string="Discount")
    disc_perc = fields.Char(string="Percentage of discount")
    refund = fields.Float(string="Refund")
    other = fields.Char(string="Other")
    other_quant = fields.Float(string="Quantity")
    claim_tot = fields.Float(compute="_get_total", string="Claim total", readonly=True)

    @api.one
    @api.depends(
        'collect_mat',
        'repair_mat',
        'deliver_mat',
        'discount',
        'refund',
        'other_quant',
    )
    def _get_total(self):
        total = self.collect_mat + self.repair_mat + self.deliver_mat + self.discount + self.refund + self.other_quant
        self.claim_tot = total