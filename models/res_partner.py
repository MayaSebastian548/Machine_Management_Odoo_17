# -*- coding; utf-8 -*-
from odoo import fields, models

"""Customer Machine tab module"""


class ResPartner(models.Model):
    _inherit = "res.partner"

    machines_ids = fields.One2many(string="Machines Id", comodel_name="machine.management",
                                   inverse_name="customer_id", help="Name of Machines")

    def action_archive(self):
        res = super().action_archive()
        self.env['machine.management'].search([('customer_id', 'in', self.ids)]).write({'active': False})
        return res

    def action_unarchive(self):
        res = super().action_unarchive()
        (self.env['machine.management'].sudo().search([('customer_id', 'in', self.ids),
                                                       ('active', '=', False)]).write({'active': True}))
        return res
