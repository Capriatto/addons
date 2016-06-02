# -*- coding: utf-8 -*-
# © <2015> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock picking reports",
    "summary": "This module adds aditional stock picking reports.",
    "version": "8.0.1.0.0",
    "category": "Inventory",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "stock",
        "account",
        "sale",
        "delivery",
        "extra_layouts",
    ],
    "data": [
        "views/stock_picking_view.xml",
        "report/report_stockpicking_a4.xml",
        "report/report_stockpicking_a4_valued.xml",
        "report/report_stockpicking_a5.xml",
        "report/report_stockpicking_a5_valued.xml",
    ],
}
