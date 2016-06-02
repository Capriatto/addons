# -*- coding: utf-8 -*-
# © <2015> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Partner extra ref",
    "summary": "This module adds a sequence for customers and a different one for suppliers.",
    "version": "8.0.1.0.0",
    "category": "Partner",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "sale",
    ],
    "data": [
        "views/partner_extra_ref_view.xml",
    ],
}
