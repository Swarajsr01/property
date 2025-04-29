# -*- coding: utf-8 -*-
"""controller for snippet value get"""

from odoo import http
from odoo.http import request, route


class WebsiteProduct(http.Controller):
    @http.route('/get_properties_categories', auth="public", type='json',
                website=True, methods=['POST'])
    def get_properties_category(self):
        """Get the properties for the snippet."""
        currency_symbol = request.env.company.currency_id.symbol
        properties_ids = request.env[
            'property.management'].sudo().search([], order='id desc')
        properties = []
        for property_id in properties_ids:
            properties.append({'id': property_id.id,
                               'image': property_id.image,
                               'name': property_id.name,
                               'owner': property_id.owner_id.name,
                               'rent_amount': property_id.rent_amount,
                               'lease_amount': property_id.lease_amount,
                               })
        values = {
            'properties': properties,
            'currency_symbol': currency_symbol,
        }
        return values

    @route('/property/<property_id>', type='http', auth="public", website=True)
    def current_property_details(self, property_id):
        """get property details and return to the template to view the property details"""
        property_obj = request.env['property.management'].sudo().browse(int(property_id))
        property_state = dict(property_obj.fields_get()['state']['selection']).get(property_obj.state)
        return request.render('property.property_view_template', {'property': property_obj,
                                                                  'state': property_state})
