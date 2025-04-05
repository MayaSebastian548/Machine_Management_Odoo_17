# -*- coding; utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteList(http.Controller):
    @http.route(['/servicelist'], type='http', auth="user", website=True)
    def service_value(self):
        website_requests = request.env['machine.service'].sudo().search([('website', '=', True)])
        values = {
            'website_requests': website_requests
        }
        return request.render("machine_management.online_service_list", values)
