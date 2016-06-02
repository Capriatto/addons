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
from .log import Log


class PaymentConverterSpain(object):
    def digits_only(self, cc_in):
        """Discards non-numeric chars"""
        cc = ""
        for i in cc_in or '':
            try:
                int(i)
                cc += i
            except ValueError:
                pass
        return cc

    def to_ascii(self, text):
        """Converts special characters such as those with accents to their
        ASCII equivalents"""
        old_chars = ['á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù', 'ä',
                     'ë', 'ï', 'ö', 'ü', 'â', 'ê', 'î', 'ô', 'û', 'Á', 'É',
                     'Í', 'Ú', 'Ó', 'À', 'È', 'Ì', 'Ò', 'Ù', 'Ä', 'Ë', 'Ï',
                     'Ö', 'Ü', 'Â', 'Ê', 'Î', 'Ô', 'Û', 'ñ', 'Ñ', 'ç', 'Ç',
                     'ª', 'º', '·', '\n']
        new_chars = ['a', 'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o', 'u', 'a',
                     'e', 'i', 'o', 'u', 'a', 'e', 'i', 'o', 'u', 'A', 'E',
                     'I', 'U', 'O', 'A', 'E', 'I', 'O', 'U', 'A', 'E', 'I',
                     'O', 'U', 'A', 'E', 'I', 'O', 'U', 'n', 'N', 'c', 'C',
                     'a', 'o', '.', ' ']
        for old, new in zip(old_chars, new_chars):
            text = text.replace(unicode(old, 'UTF-8'), new)
        return text

    def convert_text(self, text, size, justified='left'):
        if justified == 'left':
            return self.to_ascii(text)[:size].ljust(size)
        else:
            return self.to_ascii(text)[:size].rjust(size)

    def convert_float(self, number, size):
        text = str(int(round(number * 100, 0)))
        if len(text) > size:
            raise Log(_('Error:\n\nCan not convert float number %(number).2f '
                        'to fit in %(size)d characters.') % {
                'number': number,
                'size': size
            })
        return text.zfill(size)

    def convert_int(self, number, size):
        text = str(number)
        if len(text) > size:
            raise Log(_('Error:\n\nCan not convert integer number %(number)d '
                        'to fit in %(size)d characters.') % {
                'number': number,
                'size': size
            })
        return text.zfill(size)

    def convert(self, value, size, justified='left'):
        if not value:
            return self.convert_text('', size)
        elif isinstance(value, float):
            return self.convert_float(value, size)
        elif isinstance(value, int):
            return self.convert_int(value, size)
        else:
            return self.convert_text(value, size, justified)

    def convert_bank_account(self, value, partner_name):
        ccc = self.digits_only(value)
        return ccc

    def bank_account_parts(self, value, partner_name):
        ccc = self.digits_only(value)
        if len(ccc) == 20:
            return {'bank': ccc[:4],
                    'office': ccc[4:8],
                    'dc': ccc[8:10],
                    'account': ccc[10:]}
        if len(ccc) != 20:
            return {'bank': ccc[2:4],
                    'office': ccc[4:10],
                    'dc': ccc[10:12],
                    'account': ccc[12:]}

