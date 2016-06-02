# -*- coding: utf-8 -*-

from openerp.osv import orm

class ResPartner(orm.Model):

    _inherit = 'res.partner'

    def create(self, cr, uid, vals, context=None):
        context = context or {}
        if not vals.get('ref') and vals.get('customer') and self._needsRef(cr, uid, vals=vals, context=context):
            vals['ref'] = self.pool.get('ir.sequence').next_by_code(cr, uid, 'res.partner.sequence')
        if not vals.get('ref') and vals.get('supplier') and self._needsRef(cr, uid, vals=vals, context=context):
            vals['ref'] = self.pool.get('ir.sequence').next_by_code(cr, uid, 'res.partner.prov.sequence')
        return super(ResPartner, self).create(cr, uid, vals, context)

    def _needsRef(self, cr, uid, id=None, vals=None, context=None):
        if not vals and not id:
            raise Exception('Either field values or an id must be provided.')
        if id:
            vals = self.read(cr, uid, id, ['parent_id', 'is_company'], context=context)
        return vals.get('is_company') or not vals.get('parent_id')

    def _commercial_fields(self, cr, uid, context=None):
        return super(ResPartner, self)._commercial_fields(cr, uid, context=context) + ['ref']