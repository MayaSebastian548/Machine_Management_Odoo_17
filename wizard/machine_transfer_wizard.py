# -*- coding; utf-8 -*-
import io
import json
import xlsxwriter
from odoo import fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils, date, datetime


class MachineTransferWizard(models.TransientModel):
    """TransientModel for the wizard"""
    _name = "machine.transfer.wizard"
    _description = "Machine Transfer Wizard"

    from_date = fields.Date(string="From Date", help="This wizard will generate PDF Report based on this from date")
    to_date = fields.Date(string="To Date", help="This wizard will generate PDF Report based on this to date")
    customer_id = fields.Many2one(string="Customer", comodel_name="res.partner",
                                  help="Name of the Customer")
    machine_id = fields.Many2one(string="Machine Name", comodel_name="machine.management",
                                 help="Name of the Machine")

    def _check_to_date_from_date(self):
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError("From Date must be greater than To Date")

    def get_query(self):
        query = """SELECT m.serial_no, m.name as machine, c.name, t.transfer_date, t.transfer_type, t.states
                FROM machine_transfer AS t
                INNER JOIN machine_management AS m ON t.machine_id = m.id
                INNER JOIN res_partner AS c ON t.customers_id = c.id
                WHERE 1=1"""
        params = ()
        if self.from_date and self.to_date:
            query += " AND t.transfer_date >= %s"
            params += (self.from_date,)
        if self.to_date:
            query += "  AND t.transfer_date <= %s"
            params += (self.to_date,)
        if self.machine_id:
            query += "  AND t.machine_id = %s"
            params += (self.machine_id.id,)
        if self.customer_id:
            query += "  AND t.customers_id = %s"
            params += (self.customer_id.id,)
        self.env.cr.execute(query, params)

    def generate_transfer_pdf(self):
        self._check_to_date_from_date()
        self.get_query()
        report = self.env.cr.dictfetchall()
        data = {'report': report}
        if report:
            return self.env.ref('machine_management.action_report_machine_transfer').report_action(None, data=data)
        else:
            raise UserError("No data to print")

    def generate_transfer_xl(self):
        self._check_to_date_from_date()
        self.get_query()
        report = self.env.cr.dictfetchall()
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'machine': self.machine_id.id,
            'customer': self.customer_id.id,
            'report': report
        }
        if report:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'machine.transfer',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Machine Transfer Excel Report',
                         },
                'report_type': 'xlsx',
            }
        else:
            raise UserError("No data to print")

    def get_xlsx_report(self, data, response):
        today = date.today()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        date_format = workbook.add_format({'align': 'center', 'num_format': 'mm/dd/yyyy'})
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True})
        txt = workbook.add_format({'font_size': '12px', 'align': 'center'})
        sheet.set_column('B:Q', 18)
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '15px'})
        sheet.merge_range('C2:G3', 'MACHINE TRANSFER REPORT', head)
        sheet.write('B5', 'From Date:', cell_format)
        if data['from_date']:
            from_date = data['from_date']
            from_dates = datetime.strptime(from_date, '%Y-%m-%d').date()
            sheet.write('C5', from_dates, date_format)
        else:
            sheet.write_datetime('C5', today, date_format)
        sheet.write('E5', 'To Date:', cell_format)
        if data['to_date']:
            to_date = data['to_date']
            to_dates = datetime.strptime(to_date, '%Y-%m-%d').date()
            sheet.write('F5', to_dates, date_format)
        else:
            sheet.write_datetime('F5', today, date_format)
        sheet.write('B6', 'Machine:', cell_format)
        if data['machine']:
            sheet.write('C6', data['machine'], txt)
        else:
            sheet.write('C6', None, txt)
        sheet.write('E6', 'Customer:', cell_format)
        if data['customer']:
            sheet.write('F6', data['customer'], txt)
        else:
            sheet.write('C6', None, txt)
        sheet.write('B8', 'Machine Serial No.', cell_format)
        sheet.write('C8', 'Machine', cell_format)
        sheet.write('D8', 'Customer', cell_format)
        sheet.write('E8', 'Transfer Date', cell_format)
        sheet.write('F8', 'Transfer Type', cell_format)
        sheet.write('G8', 'State', cell_format)
        for i, re in enumerate(data['report'], start=9):
            transfer = re['transfer_date']
            tr_date = datetime.strptime(transfer, '%Y-%m-%d').date()
            types = ''
            sheet.write(f'B{i}', re['serial_no'], txt)
            sheet.write(f'C{i}', re['machine'], txt)
            sheet.write(f'D{i}', re['name'], txt)
            sheet.write_datetime(f'E{i}', tr_date, date_format)
            if re['transfer_type'] == 'install':
                types = "Install"
            sheet.write(f'F{i}', types, txt)
            if re['states'] == 'new':
                state = "New"
            else:
                state = "Done"
            sheet.write(f'G{i}', state, txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
