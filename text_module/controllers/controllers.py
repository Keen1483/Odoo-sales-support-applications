# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class TextModule(http.Controller):
    @http.route('/text_module/text_module/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/text_module/text_module/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('text_module.listing', {
            'root': '/text_module/text_module',
            'objects': http.request.env['text_module.text_module'].search([]),
        })

    @http.route('/text_module/text_module/objects/<model("text_module.text_module"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('text_module.object', {
            'object': obj
        })

    @http.route('/my_sale_details', type='http', auth='public', website=True)
    def sale_details(self, **kwargs):
        sale_details = request.env['sale.order'].sudo().search([])
        return request.render('text_module.sale_details_page', {'my_details': sale_details})
