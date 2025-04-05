# -*- coding; utf-8 -*-

from datetime import date
from odoo import api, fields, models
from odoo.exceptions import UserError


class MachineTransfer(models.Model):
    """Machine transfer Model table name in database"""
    _name = "machine.transfer"
    _description = "Machine Transfer"
    _rec_name = "machine_id"

    alert_msg = fields.Char(readonly=True, string="Alert Message for transfer")
    machine_id = fields.Many2one(string="Machine", comodel_name="machine.management",
                                 help="Name of the Machine", required=True,
                                 domain="[('id','in',machine_filters_ids)]")
    machine_serial_no = fields.Integer(string="Serial Number",
                                       related="machine_id.serial_no", help="Unique Serial number for the machine")
    transfer_date = fields.Date(string="Transfer Date", default=date.today(), help="Date of transfers")
    transfer_type = fields.Selection(
        selection=[('install', 'Install'), ('remove', 'Remove')], string="Transfer Type",
        help="Type of Transfer", default='install', domain=[('machine_filters_id', '=', 'machine_id')])
    customers_id = fields.Many2one(string="Customer", comodel_name="res.partner",
                                   help="Name of the Customer")
    internal_notes = fields.Html(string="Internal Notes", help="Internal notes about the machine")
    states = fields.Selection(
        selection=[('new', 'New'), ('done', 'Done')], default="new",
        help="State of transfer", string="State of machine transfer")
    hide = fields.Boolean(string='Hide', help="Boolean field for hiding alert message")
    machine_filters_ids = fields.Many2many(string="Machine filter", help="Filter machines ",
                                           comodel_name="machine.management",
                                           compute="_compute_machine_filters_ids", store=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    active = fields.Boolean(string="Active", default=True, help="Boolean field for archive and unarchive")

    def submit(self):
        """Submit function in machine transfer"""
        if self.transfer_type == 'remove':
            if self.machine_id.state == 'active':
                raise UserError("Machine is in Active State")
            self.machine_id.write({'state': 'active'})
        elif self.transfer_type == 'install':
            if self.machine_id.state == 'inservice':
                raise UserError("Machine is in In service State")
            self.machine_id.write({'state': 'inservice', 'customer_id': self.customers_id})
        else:
            raise UserError("Choose transfer type")
        self.write({'states': 'done'})

    @api.onchange('transfer_type')
    def _onchange_transfer_type(self):
        """Error message when the condition is not satisfied"""
        if self.transfer_type == 'remove':
            if self.machine_id.state == 'active':
                self.write({'alert_msg': "The State is in Active. The transfer type remove cannot be applied",
                           'hide': True})
            else:
                self.write({'alert_msg': "",
                            'hide': False})
        if self.transfer_type == 'install':
            if self.machine_id.state == 'inservice':
                self.write({'alert_msg': "The State is in In Service. The transfer type install cannot be applied",
                            'hide': True})
            else:
                self.write({'alert_msg': "",
                            'hide': False})

    @api.depends('transfer_type')
    def _compute_machine_filters_ids(self):
        """function to write the active and in service machines to the machines in the machine transfer form """
        for rec in self:
            if rec.transfer_type == "install":
                active_machines = self.env['machine.management'].search([('state', '=', 'active'),
                                                                         ('company_id', '=', self.env.company.id)])
                rec.write({'machine_filters_ids': active_machines})
            elif rec.transfer_type == "remove":
                inservice_machines = self.env['machine.management'].search([('state', '=', 'inservice'),
                                                                            ('company_id', '=', self.env.company.id)])
                rec.write({'machine_filters_ids': inservice_machines})
