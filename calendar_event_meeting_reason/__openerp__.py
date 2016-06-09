# -*- coding: utf-8 -*-
# © <2016> <SANDRA FIGUEROA VARELA sandrafigvar@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Calendar event meeting reason",
    "summary": "This module adds meeting reasons to calendar.event model.",
    "version": "8.0.1.0.0",
    "category": "Inventory",
    "author": "Sandra Figueroa Varela",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "calendar",
    ],
    #TO DO - Add reasons as data, and let user introduce more reasons
    "data": [
        "views/meeting_reason_view.xml",
    ],
}
