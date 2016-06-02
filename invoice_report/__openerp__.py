# -*- coding: utf-8 -*-
# © <2015> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Invoice report",
    "summary": "This module modifies the default invoice report.",
    "version": "8.0.1.0.0",
    "category": "Invoicing",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "views/invoice_report_view.xml",
    ],
}
