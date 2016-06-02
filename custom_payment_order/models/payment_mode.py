# -*- coding: utf-8 -*-
# © <2008> <ZIKZAKMEDIA S.L. http://zikzakmedia.com>
#          <Jordi Esteve jesteve@zikzakmedia.com>
# © <2008> <ACYSOS SL>
#          <Ignacio Ibeas ignacio@acysos.com>
# © <2008> <Pablo Rocandio>
# © <2011-2012> <Ainara Galdona www.advanzosc.com>
# © <2013> <Serv. Tecnol. Avanzados http://www.serviciosbaeza.com>
#          <Pedro M. Baeza pedro.baeza@serviciosbaeza.com>
# © <2016> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class PaymentMode(models.Model):
    _inherit = "payment.mode"

    pagos_suffix = fields.Char(string='Suffix', size=3, default='000')
    pagos_require_bank_account = fields.Boolean(
        string='Require bank account', default=True,
        help='If your bank allows you to send orders without the bank account '
        'info, you may disable this option')
    pagosprov_type = fields.Selection(
        string='Type of payment', default='transfer',
        selection=[('transfer', 'Transfer'),
                   ('promissory_note', 'Promissory Note'),
                   ('cheques', 'Cheques'),
                   ('certified_payments', 'Certified Payments')])
    pagosprov_text1 = fields.Char(
        string='Line 1', size=36,
        help='Enter text and/or select a field of the invoice to include as a '
        'description in the letter. The possible values ​​are: ${amount}, '
        '${communication}, {communication2}, {date}, {ml_maturity_date}, '
        '{create_date}, {ml_date_created}')
    pagosprov_text2 = fields.Char(
        string='Line 2', size=36,
        help='Enter text and/or select a field of the invoice to include as a '
        'description in the letter. The possible values ​​are: ${amount}, '
        '${communication}, {communication2}, {date}, {ml_maturity_date}, '
        '{create_date}, {ml_date_created}')
    pagosprov_text3 = fields.Char(
        string='Line 3', size=36,
        help='Enter text and/or select a field of the invoice to include as a '
        'description in the letter. The possible values ​​are: ${amount}, '
        '${communication}, {communication2}, {date}, {ml_maturity_date}, '
        '{create_date}, {ml_date_created}')
    pagosprov_payroll_check = fields.Boolean(
        string='Payroll Check',
        help='Check it if you want to add the 018 data type in the file (the '
        'vat of the recipient is added in the 018 data type).')
    pagosprov_add_date = fields.Boolean(
        string='Add Date',
        help='Check it if you want to add the 910 data type in the file to '
        'include the payment date.')
    pagosprov_send_type = fields.Selection(
        string='Send type', default='mail',
        help='The sending type of the payment file',
        selection=[('mail', 'Ordinary Mail'),
                   ('certified_mail', 'Certified Mail'),
                   ('other', 'Other')])
    pagosprov_not_to_the_order = fields.Boolean(string='Not to the Order',
                                            default=True)
    pagosprov_barred = fields.Boolean(string='Barred', default=True)
    pagosprov_cost_key = fields.Selection(
        string='Concept of the Order', default='payer',
        selection=[('payer', 'Expense of the Payer'),
                   ('recipient', 'Expense of the Recipient')])
    pagosprov_concept = fields.Selection(
        string='Concept of the order', default='other',
        selection=[('payroll', 'Payroll'), ('pension', 'Pension'),
                   ('other', 'Other')])
    pagosprov_direct_pay_order = fields.Boolean(
        string='Direct Pay Order', default=False, help='By default "Not"')
    is_pagosprov = fields.Boolean(compute="_compute_is_pagosprov")

    @api.multi
    @api.depends('type')
    def _compute_is_pagosprov(self):
        pagosprov_type = self.env.ref('custom_payment_order.export_pagosprov')
        for record in self:
            record.is_pagosprov = record.type == pagosprov_type
