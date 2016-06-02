# -*- coding: utf-8 -*-
# © <2015> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Invoice letter",
    "summary": "This module adds a report that is sent as a letter with the invoice.",
    "version": "8.0.1.0.0",
    "category": "Accounting",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "account",
        "report",
    ],
    "data": [
        "views/invoice_letter_view.xml",
        "report/report_invoice_letter.xml",
    ],
}
