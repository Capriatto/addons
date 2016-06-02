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

from openerp import _
from datetime import datetime
from .log import Log
import time
from .converter import PaymentConverterSpain


class PagosProv(object):
    

    def __init__(self, env):
        self.env = env

    def get_message(self, recibo, message=None):
        """
        Evaluates an expression and returns its value
        @param recibo: Order line data
        @param message: The expression to be evaluated
        @return: Computed message (string)
        """
        fields = [
            'name',
            'amount',
            'communication',
            'communication2',
            'date',
            'ml_maturity_date',
            'create_date',
            'ml_date_created',
            'ml_inv_ref'
        ]
        if message is None or not message:
            message = ''
        for field in fields:
            if type(recibo[field]) == str:
                value = unicode(recibo[field], 'UTF-8')
            elif type(recibo[field]) == unicode:
                value = recibo[field]
            else:
                value = str(recibo[field])
            message = message.replace('${' + field + '}', value)
        return message

    def _start_pp(self):
        converter = PaymentConverterSpain()
        vat = self.order.mode.bank_id.partner_id.vat[2:]
        ref = self.order.mode.bank_id.partner_id.ref
        suffix = self.order.mode.pagos_suffix
        return converter.convert(vat + suffix, 12)

    def _cabecera_ordenante_pp(self):
        converter = PaymentConverterSpain()
        today = datetime.today().strftime('%d%m%Y')
        
        text = ''

        # Primer tipo
        text += '13620'
        text += self._start_pp() 
        text += 9*' ' 
        text += '001'
        text += today
        if self.order.date_scheduled:
            planned = datetime.strptime(self.order.date_scheduled, '%Y-%m-%d')
            text += planned.strftime('%d%m%Y')
        else:
            text += today
        ccc = converter.bank_account_parts(self.order.mode.bank_id.acc_number,
                                           self.order.mode.partner_id.name)
        text += ccc['bank']
        text += ccc['office']
        text += ccc['account']
        text += '0'
        text += 3*' '
        text += ccc['dc']
        text += 3*' ' 
        text += '\r\n'

        # Segundo Tipo
        text += '13620'
        text += self._start_pp()
        text += 9*' '
        text += '002'
        text += converter.convert(self.order.mode.bank_id.partner_id.name, 36)
        text += 7*' '
        text += '\r\n'

        # Tercer Tipo
        text += '13620'
        text += self._start_pp()
        text += 9*' '
        text += '003'
        # Direccion
        partner_model = self.env['res.partner']
        address_ids = self.order.mode.bank_id.partner_id.address_get(
            ['invoice', 'default'])
        if address_ids.get('invoice'):
            address = partner_model.browse(address_ids['invoice'])
        elif address_ids.get('default'):
            address = partner_model.browse(address_ids['default'])
        else:
            raise Log(_('User error:\n\nCompany %s has no invoicing or '
                        'default address.') %
                      self.order.mode.bank_id.partner_id.name)
        text += converter.convert(address.city, 12)
        text += 31*' '
        text += '\r\n'

        # Cuarto Tipo
        text += '13620'
        text += self._start_pp()
        text += 9*' '
        text += '004'
        text += 'ANTONIO PALACIOS'
        text += 27*' '
        text += '\r\n'
        if len(text) % 74 != 0:
            raise Log(_('Configuration error:\n\nA line in "%s" is not 72 '
                        'characters long:\n%s') % ('Cabecera ordenante pp',
                                                   text), True)
        return text


    def _detalle_nacionales_pp(self, recibo, pagosprov_type):
        converter = PaymentConverterSpain()
        if recibo['partner_id'].vat == 0:
            raise Log(_('User error:\n\nPartner %s has no vat') % recibo['partner_id'].name)
        vat = recibo['partner_id'].vat[2:]
        partner_model = self.env['res.partner']
        address_ids = recibo['partner_id'].address_get(
            ['invoice', 'default'])
        if address_ids.get('invoice'):
            address = partner_model.browse(address_ids['invoice'])
        elif address_ids.get('default'):
            address = partner_model.browse(address_ids['default'])
        else:
            raise Log(_('User error:\n\nPartner %s has no invoicing or '
                        'default address.') % recibo['partner_id'].name)
        # Primer Registro
        text = ''
        text += '16620'
        text += self._start_pp()
        text += vat
        text += '010'
        text += converter.convert(abs(recibo['amount']), 12)
        vcto = datetime.strptime(recibo['ml_maturity_date'], '%Y-%m-%d')
        text += 23*' '
        text += vcto.strftime('%d%m%Y')
        text += '\r\n'
        # Segundo Registro
        text += '16620'
        text += self._start_pp()
        text += vat
        text += '011'
        text += converter.convert(recibo['partner_id'].name, 43)
        text += '\r\n'
        # Tercer y Cuarto Registro
        lines = []
        if address.street:
            lines.append(("012", address.street))
        if len(address.street) > 36:
            lines.append(("013", address.street[36:]))
        else:
            lines.append(("013", address.city))
        for (code, street) in lines:
            text += '16620'
            text += self._start_pp()
            text += vat
            text += code
            text += converter.convert(street, 36)
            text += 7*' '
            text += '\r\n'

            
        # Quinto Registro
        if address.zip:
            text += '16620'
            text += self._start_pp()
            text += vat
            text += '014'
            text += converter.convert(address.zip, 36)
            text += 7*' '
            text += '\r\n'

        if address.state_id.name:
            text += '16620'
            text += self._start_pp()
            text += vat
            text += '015'
            text += converter.convert(address.state_id.name, 36)
            text += 7*' '
            text += '\r\n'
        
        # Registro
        veces = len(recibo['communication']) #ya no se usa
        sufijo = 100
        pagos = len(self.order.line_ids) #Numero de lineas de pago en la orden de pago
        for i in range(pagos):
            if self.order.line_ids[i].partner_id == recibo['partner_id']:
                text += '17620'
                text += self._start_pp()
                text += vat
                text += str(sufijo)
                sufijo += 1
                prueba = datetime.strptime(self.order.line_ids[i].ml_inv_ref.date_invoice, '%Y-%m-%d')
                text += prueba.strftime('%d%m%Y')
                text += converter.convert(recibo['partner_id'].ref, 8)
                text += 2*' '
                if self.order.line_ids[i].ml_inv_ref.reference == 0:
                    raise Log(_('User error:\n\nInvoice %s has no payment reference') % self.order.line_ids[i].ml_inv_ref.number)
                if len(self.order.line_ids[i].ml_inv_ref.reference) >= 12:
                    text += converter.convert(self.order.line_ids[i].ml_inv_ref.reference, 12)
                else:
                    text += converter.convert(' ', 12-len(self.order.line_ids[i].ml_inv_ref.reference))+self.order.line_ids[i].ml_inv_ref.reference
                text += converter.convert(abs(self.order.line_ids[i].ml_inv_ref.amount_total), 12)
                text += ' '
                text += '\r\n'
        if len(text) % 74 != 0:
            raise Log(_('Configuration error:\n\nA line in "%s" is not 72 '
                        'characters long:\n%s') % ('Detalle nacionales pp',
                                                   text), True)
                     
        return text

    def _total_general_pp(self, values):
        converter = PaymentConverterSpain()
        text = '18620'
        text += 'B36029080'
        text += 15*' '
        text += converter.convert(self.order.total, 12)
        text += converter.convert(values[0], 8)
        text += converter.convert(values[1], 10)
        text += 13*' '
        text += '\r\n'
        if len(text) != 74:
            raise Log(_('Configuration error:\n\nThe line "%s" is not 72 '
                        'characters long:\n%s') % ('Total general pp',
                                                   text), True)
        return text

    def create_file(self, order, lines):
        self.order = order
        payment_line_count = 0
        record_count = 0
        txt_file = ''
        txt_file += self._cabecera_ordenante_pp()
        
        for recibo in lines:
            text = self._detalle_nacionales_pp(recibo, order.mode.pagosprov_type)
            txt_file += text
            record_count += len(text.split('\r\n'))-1
            payment_line_count += 1
            
        values = (payment_line_count, record_count + 2)
        record_count = len(txt_file.split('\r\n'))
        values = (payment_line_count, record_count)
        txt_file += self._total_general_pp(values)
        return txt_file


