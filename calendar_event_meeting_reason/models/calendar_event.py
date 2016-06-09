# -*- coding: utf-8 -*-

from openerp import models, fields, api

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    meeting_reason_id = fields.Many2one(
    	'calendar.event.meeting.reason',
    	string="Meeting reason",
    	readonly=True,
    	ondelete="restrict")

class CalendarEventMeetingReason(models.Model):
	_name = 'calendar_event_meeting_reason'
	_description = 'Calendar Event Meeting Reason'

	name = fields.Char('Reason', required=False, translate=True)
