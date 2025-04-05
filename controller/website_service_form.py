# -*- coding; utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    @http.route(['/service'], type='http', auth="user", website=True)
    def service_machines(self):
        machines = request.env['machine.management'].search([('state', '=', 'inservice')])
        values = {'machines': machines}
        return request.render("machine_management.online_service_form", values)
