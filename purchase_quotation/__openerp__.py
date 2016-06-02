# -*- coding: utf-8 -*-
# © <2015> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Quotation",
    "summary": "This module modifies the existing purchase order report.",
    "version": "8.0.1.0.0",
    "category": "Purchase",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "purchase",
        "extra_layouts",
    ],
    "data": [
        "views/purchase_quotation_view.xml",
    ],
}
