# -*- coding; utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteMachineInfo(http.Controller):
    @http.route(['/machine_info/<int:machine_id>/'], type='http', auth="user", website=True)
    def service_machines(self, machine_id):
        machine = request.env['machine.management'].sudo().browse(machine_id)
        values = {'machines': machine}
        return request.render("machine_management.machine_info_website_form", values)
