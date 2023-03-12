# -*- coding: utf-8 -*-
from odoo import http

# class WebFavicon(http.Controller):
#     @http.route('/web_favicon/web_favicon/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/web_favicon/web_favicon/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('web_favicon.listing', {
#             'root': '/web_favicon/web_favicon',
#             'objects': http.request.env['web_favicon.web_favicon'].search([]),
#         })

#     @http.route('/web_favicon/web_favicon/objects/<model("web_favicon.web_favicon"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('web_favicon.object', {
#             'object': obj
#         })