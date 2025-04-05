# -*- coding; utf-8 -*-
from odoo import fields, models
"""Machine tags module"""


class MachineTags(models.Model):

    """Machine tags Model table name in database"""
    _name = "machine.tags"
    _description = "Machine Tags"
    _rec_name = "machine_tags"

    machine_tags = fields.Char(string="Machine tags", help="Tags for the machine")
