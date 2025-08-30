# -*- coding: utf-8 -*-
# from odoo import http


# class Geotek(http.Controller):
#     @http.route('/geotek/geotek', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/geotek/geotek/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('geotek.listing', {
#             'root': '/geotek/geotek',
#             'objects': http.request.env['geotek.geotek'].search([]),
#         })

#     @http.route('/geotek/geotek/objects/<model("geotek.geotek"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('geotek.object', {
#             'object': obj
#         })

