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
{
    "name": "Custom payment order",
    "summary": "This module allows to export custom payment order.",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "account_direct_debit",
    ],
    "data": [
        "wizard/export_pagos_view.xml",
        "data/payment_type_pagos.xml",
        "views/payment_mode_view.xml",
    ],
}
