# -*- coding; utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteSnippetMachine(http.Controller):
    @http.route(['/machine_snippet'], type='json', auth="user", website=True)
    def get_machine(self):
        machines = request.env['machine.management'].search_read([],
                                                                 ['sequence_no', 'name', 'date_of_purchase',
                                                                  'purchase_value', 'image', 'currency_id'])
        machine_list = [machines[i: i + 4] for i in range(0, len(machines), 4)]
        return machine_list
