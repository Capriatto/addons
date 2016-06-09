# -*- coding: utf-8 -*-

from openerp import models, fields, api

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    reason = fields.Selection([
    	('request', "Customer request"),
    	('quotation', "Quotation request"),
    	('followup', "Follow up"),
    	('handover', "Hand over quotation"),
    ], string="Meeting reason")
