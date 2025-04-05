# -*- coding; utf-8 -*-
from odoo import fields, models
"""Machine type module"""


class MachineType(models.Model):

    """Machine type Model table name in database"""
    _name = "machine.type"
    _description = "Machine Type"
    _rec_name = "machine_type"

    machine_type = fields.Char(string="Machine Type", help="Type of machines")
