# -*- coding; utf-8 -*-
import base64
from odoo import http
from odoo.http import request


class WebsiteServiceForm(http.Controller):
    @http.route(['/serviceform/<int:machine_id>/'], type='http', auth="user", website=True)
    def service_form(self, machine_id):
        partners = request.env['res.partner'].sudo().search([])
        machine = request.env['machine.management'].sudo().browse(machine_id)
        values = {
            'partners': partners,
            'machines': machine,
        }
        return request.render("machine_management.online_website_service_form", values)

    @http.route('/service/submit', type='http', auth="public", website=True)
    def create_service(self, **kw):
        machine = request.env['machine.management'].sudo().search([('name', '=', kw.get('machine_id', False))])
        company = request.env['res.company'].sudo().search([('name', '=', kw.get('company_id', False))])
        file = kw.get('attachment', False)
        file_bytes = file.encode("ascii")
        base64_file = base64.b64encode(file_bytes)
        request.env['machine.service'].sudo().create({
            'machines_id': machine.id,
            'customer_id': kw.get('customer_id', False),
            'company_id': company.id,
            'date_of_service': kw.get('date_of_service', False),
            'attachment': base64_file,
            'description': kw.get('description', False),
            'website': True,
        })
        website_requests = request.env['machine.service'].sudo().search([('website', '=', True)])
        values = {
            'website_requests': website_requests
        }
        return request.render("machine_management.online_service_list", values)
