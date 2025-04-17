# -*- coding: utf-8 -*-
"""webiste for property management"""

from odoo import http
from odoo.http import request
import re


class PropertyRentController(http.Controller):
    @http.route(['/property'], type="http", auth="public", website=True)
    def display_properties(self, **kwargs):
        def group_list(lst, n):
            return [lst[i:i + n] for i in range(0, len(lst), n)]

        properties = request.env['property.management'].sudo().search([])
        grouped_properties = group_list(properties, 4)
        values = {
            'records': grouped_properties
        }
        return request.render("property.properties_website_template", values)

    @http.route('/property/<string:slug>', auth='public', website=True)
    def display_property(self, slug):
        match = re.search(r'-(\d+)$', slug)
        if not match:
            return request.not_found()
        property_id = int(match.group(1))
        property = request.env['property.management'].sudo().search([('id', '=', property_id)])
        values = {
            'records': property
        }
        return request.render("property.property_website_template", values)



