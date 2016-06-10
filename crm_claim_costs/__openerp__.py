# -*- coding: utf-8 -*-
# © <2016> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Crm claim costs",
    "summary": "Keep track of claim costs",
    "version": "8.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "sale",
        "crm_claim",
    ],
    "data": [
        "views/crm_claim_costs_view.xml",
    ],
}
