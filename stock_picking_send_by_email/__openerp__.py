# -*- coding: utf-8 -*-
# © <2015> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock picking send by email",
    "summary": "This module allows to send the picking report by email.",
    "version": "8.0.1.0.0",
    "category": "Warehouse Management",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "stock",
        "email_template",
        "stock_picking_reports",
    ],
    "data": [
        "views/stock_picking_view.xml",
        "views/stock_picking_mail.xml",
    ],
}
