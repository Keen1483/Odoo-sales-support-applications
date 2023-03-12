# -*- coding: utf-8 -*-
from odoo import http

# class UnjustifiedTicket(http.Controller):
#     @http.route('/unjustified_ticket/unjustified_ticket/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/unjustified_ticket/unjustified_ticket/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('unjustified_ticket.listing', {
#             'root': '/unjustified_ticket/unjustified_ticket',
#             'objects': http.request.env['unjustified_ticket.unjustified_ticket'].search([]),
#         })

#     @http.route('/unjustified_ticket/unjustified_ticket/objects/<model("unjustified_ticket.unjustified_ticket"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('unjustified_ticket.object', {
#             'object': obj
#         })