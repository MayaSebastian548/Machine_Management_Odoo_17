# -*- coding; utf-8 -*-
from odoo import api, models


class MachineTransferReport(models.AbstractModel):
    """Abstract Model for the report"""
    _name = 'report.machine_management.report_machine_transfer'
    _description = "Machine Transfer Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'data': data,
        }
