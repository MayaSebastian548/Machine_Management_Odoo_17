# -*- coding; utf-8 -*-
from odoo import fields, models
from datetime import datetime
"""Machine Service Model"""


class MachineService(models.Model):
    _name = "machine.service"
    _description = "Machine Service"
    _rec_name = "machines_id"

    machines_id = fields.Many2one(string="Machines", comodel_name="machine.management",
                                  required=True, help="Name of the Machine")
    machine_serial_no = fields.Integer(string="Serial Number",
                                       related="machines_id.serial_no", help="Serial number for the machine")
    customer_id = fields.Many2one(string="Customer", help="Name of the customer", comodel_name="res.partner",
                                  readonly=True, related="machines_id.customer_id")
    date_of_service = fields.Date(string="Date of Service", help="Service Date of the Machines",
                                  default=datetime.today())
    description = fields.Text(help="Description about the machine service", string="Description")
    internal_note = fields.Html(help="Internal note for the Machine service", string="Internal Note")
    tech_person_ids = fields.Many2many(string="Technical Person",
                                       comodel_name="res.partner",
                                       help="Technical person for this service")
    service_state = fields.Selection(
        selection=[('open', 'Open'), ('started', 'Started'), ('done', 'Done'), ('cancel', 'Cancel')],
        default="open", help="State of Machine Service", string="Service State")
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company,
                                 readonly=True)
    parts_consumed_ids = fields.One2many(comodel_name="machine.parts", inverse_name="service_id",
                                         string="Consumed Parts", help="Consumed products for the machine service")
    active = fields.Boolean(string="Active", default=True, help="Boolean field for archive and unarchive")
    attachment = fields.Binary(string="Attachment", help="Attachment for the machine service")
    website = fields.Boolean(string="Website", default=False, help="Boolean field for service created through website")

    def start_case(self):
        self.write({'service_state': 'started'})
        (self.search(['&', ('service_state', '=', 'started'), ('company_id', '=', self.env.company.id)]).machines_id.
         sudo().filtered(lambda m: m.company_id.id == self.env.company.id).write({
            'last_service_date': self.date_of_service
            }))

    def close_case(self):
        self.write({'service_state': 'done'})
        mail_template = self.env.ref('machine_management.service_mail_template')
        mail_template.send_mail(self.id, force_send=True)

    def cancel_case(self):
        self.write({'service_state': 'cancel'})

    def create_invoice(self):
        invoice_data = {
            'partner_id': self.customer_id.id,
            'invoice_line_ids': [],
            'move_type': 'out_invoice',
        }
        for rec in self.parts_consumed_ids:
            invoice_data['invoice_line_ids'].append((0, 0, {
                'product_id': rec.machine_parts_id.id,
                'price_unit': rec.parts_price,
                'quantity': rec.parts_quantity,
            }))
        invoice_data['invoice_line_ids'].append((0, 0, {
                'product_id': self.env.ref('machine_management.service_product_id').product_variant_id.id,
                'price_unit': self.env.ref('machine_management.service_product_id').list_price,
                'quantity': 1,
        }))
        draft = self.env['account.move'].search([
            ('partner_id', '=', self.customer_id.id),
            ('state', '=', 'draft')
        ])
        if draft:
            draft[0].write({'invoice_line_ids':  [rec for rec in invoice_data['invoice_line_ids'] if
                                                  invoice_data['invoice_line_ids']]})
            return {
                'name': "Invoice Created",
                'view_mode': 'form',
                'view_id': self.env.ref('account.view_move_form').id,
                'view_type': 'form',
                'res_model': 'account.move',
                'res_id': draft[0].id,
                'type': 'ir.actions.act_window',
            }
        invoice = self.env['account.move'].create(invoice_data)
        return {
            'name': "Invoice Created",
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'view_type': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'type': 'ir.actions.act_window',
        }
