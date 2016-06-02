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

from openerp import models, fields, api, _
from openerp import workflow
import base64
from .log import Log
from .converter import PaymentConverterSpain
from .pagosprov import PagosProv


class BankingExportPagosProvWizard(models.TransientModel):
    _name = 'banking.export.pavos.prov.wizard'
    _description = 'Exportar archivo de pagos a proveedores'

    join = fields.Boolean(
        string='Join payment lines of the same partner and bank account')
    note = fields.Text('Log')
    file = fields.Binary(string="File", readonly=True)
    filename = fields.Char(string="Filename", readonly=True)
    payment_order_ids = fields.Many2many('payment.order', readonly=True)
    state = fields.Selection(
        string='State', readonly=True, default='create',
        selection=[('create', 'Create'), ('finish', 'Finish')])

    @api.model
    def create(self, vals):
        payment_order_ids = self._context.get('active_ids', [])
        vals.update({
            'payment_order_ids': [(6, 0, payment_order_ids)],
        })
        return super(BankingExportPagosProvWizard, self).create(vals)

    @api.model
    def _get_pagos_exporter(self, payment_order):
        if payment_order.mode.type.code == 'pagosprov':
            pagosprov = PagosProv(self.env)
        else:
            raise Log(_('User error:\n\nThe payment mode is not '
                        'Pagos Prov '), True)
        return pagosprov

    @api.model
    def _check_company_bank_account(self, payment_order):
        converter = PaymentConverterSpain()
        cc = converter.digits_only(payment_order.mode.bank_id.acc_number)

    @api.model
    def _check_required_bank_account(self, payment_order, pay_lines):
        if payment_order.mode.pagos_require_bank_account:
            converter = PaymentConverterSpain()
            for line in pay_lines:
                bank = line['bank_id']
                ccc = bank and bank.acc_number or False
                ccc = converter.digits_only(ccc)

    @api.multi
    def create_pagosprov(self):
        self.ensure_one()
        form_obj = self
        try:
            payment_order = self.env['payment.order'].browse(
                self._context.get('active_id'))
            if not payment_order.line_ids:
                raise Log(_('User error:\n\nWizard can not generate export '
                            'file, there are not payment lines.'), True)
            self._check_company_bank_account(payment_order)
            pay_lines = []
            if form_obj.join:
                # Lista con todos los partners+bancos diferentes de la remesa
                partner_bank_l = reduce(
                    lambda l, x: x not in l and l.append(x) or l,
                    [(line.partner_id, line.bank_id)
                     for line in payment_order.line_ids], [])
                # Computo de la lista de pay_lines agrupados por mismo
                # partner+banco.
                # Los importes se suman, los textos se concatenan con un
                # espacio en blanco y las fechas se escoge el mбximo
                for partner, bank in partner_bank_l:
                    lineas = [recibo for recibo in payment_order.line_ids
                              if (recibo.partner_id == partner and
                                  recibo.bank_id == bank)]
                    pay_lines.append({
                        'partner_id': partner,
                        'bank_id': bank,
                        'name': partner.ref or str(partner.id),
                        'amount': reduce(lambda x, y: x+y,
                                         [l.amount for l in lineas], 0),                   
                        'communication': reduce(lambda x, y: x+' '+(y or ''),
                                                [l.name+' '+l.communication
                                                 for l in lineas], ''),
                        'communication2': reduce(lambda x, y: x+' '+(y or ''),
                                                 [l.communication2
                                                  for l in lineas], ''),
                        'date': max([l.date for l in lineas]),
                        'ml_maturity_date': max([l.ml_maturity_date
                                                 for l in lineas]),
                        'create_date': max([l.create_date for l in lineas]),
                        'ml_date_created': max([l.ml_date_created
                                                for l in lineas]),
                        'ml_inv_ref': [l.ml_inv_ref for l in lineas]
                    })
            else:
                # Cada linea de pago es un recibo
                for l in payment_order.line_ids:
                    pay_lines.append({
                        'partner_id': l.partner_id,
                        'bank_id': l.bank_id,
                        'name': l.partner_id.ref or str(l.partner_id.id),
                        'amount': l.amount,
                        'communication': l.name+' '+l.communication,
                        'communication2': l.communication2,
                        'date': l.date,
                        'ml_maturity_date': l.ml_maturity_date,
                        'create_date': l.create_date,
                        'ml_date_created': l.ml_date_created,
                        'ml_inv_ref': [l.ml_inv_ref]
                    })
            self._check_required_bank_account(payment_order, pay_lines)
            pagos = self._get_pagos_exporter(payment_order)
            txt_file = pagos.create_file(payment_order, pay_lines)
        except Log, log:
            form_obj.note = unicode(log)
            form_obj.state = 'create'
            action = {
                'name': 'Archivo Pagos Prov',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': self._name,
                'res_id': self.id,
                'target': 'new',
            }
            return action
        else:
            # Ensure line breaks use MS-DOS (CRLF) format as standards require.
            txt_file = txt_file.replace('\r\n', '\n').replace('\n', '\r\n')
            file_payment_order = base64.encodestring(txt_file.encode('utf-8'))
            # Adjuntar nuevo archivo de remesa
            filename = payment_order.mode.type.code + '_'
            filename += payment_order.reference
            self.env['ir.attachment'].create(
                {'res_model': 'payment.order',
                 'res_id': payment_order.id,
                 'name': filename,
                 'datas': file_payment_order})
            self.filename = filename
            self.file = file_payment_order
            self.state = 'finish'
        action = {
            'name': 'Archivo Pagos Prov',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'new',
        }
        return action

    @api.multi
    def save_pagos(self):
        """Save the file: send the done signal to all payment
        orders in the file. With the default workflow, they will
        transition to 'done', while with the advanced workflow in
        account_banking_payment_transfer they will transition to 'sent' waiting
        reconciliation.
        """
        self.ensure_one()
        for order in self.payment_order_ids:
            workflow.trg_validate(self.env.uid, 'payment.order', order.id,
                                  'done', self.env.cr)
        return True


