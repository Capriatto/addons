# -*- coding: utf-8 -*-
# © <2015> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale quotation",
    "summary": "This module adds a tab for quotation in the sale order form, and a quotation report.",
    "version": "8.0.1.0.0",
    "category": "Sales",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "sale",
        "extra_layouts",
        "email_template",
    ],
    "data": [
        "views/quotation_mail.xml",
        "views/sale_quotation_report.xml",
        "views/sale_quotation_view.xml",
        "report/report_quotation.xml",
    ],
}
