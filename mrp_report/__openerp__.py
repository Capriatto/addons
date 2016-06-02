# -*- coding: utf-8 -*-
# © <2015> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "MRP report",
    "summary": "This module modifies the existing mrp report.",
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "mrp",
        "extra_layouts",
    ],
    "data": [
        "views/mrp_report_view.xml",
    ],
}
