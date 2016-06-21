# -*- coding: utf-8 -*-
# © <2016> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale extra state",
    "summary": "This module adds an adittional state to the sales order.",
    "version": "8.0.1.0.0",
    "category": "Sales",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "sale",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/sale_order_workflow.xml",
    ],
}
