# -*- coding: utf-8 -*-
# © <2015> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock group by customer",
    "summary": "This module adds a 'group by' option to group the picking order by customer.",
    "version": "8.0.1.0.0",
    "category": "Stock",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "sale",
        "stock",
    ],
    "data": [
        "views/group_by_customer_view.xml",
    ],
}
