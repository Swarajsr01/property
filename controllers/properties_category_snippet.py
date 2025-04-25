from odoo import http
from odoo.http import request, route


class WebsiteProduct(http.Controller):
    @http.route('/get_properties_categories', auth="public", type='json',
                website=True, methods=['POST'])
    def get_properties_category(self):
        """Get the website categories for the snippet."""
        print("345678")
        # properties_ids = request.env[
        #     'property.management'].sudo().search_read([], order='id desc')
        properties_ids = request.env[
            'property.management'].sudo().search([], order='id desc')
        properties = []
        for property in properties_ids:
            properties.append({'id': property.id,
                               'image': property.image,
                               'name': property.name,
                               'owner': property.owner_id.name,
                               'rent_amount': property.rent_amount,
                               'lease_amount': property.lease_amount,
                               })
        values = {
            'properties': properties,
        }
        return values

    @route('/property/<property_id>', type='http', auth="user", website=True)
    def current_property_details(self, property_id):
        property_obj = request.env['property.management'].sudo().search([('id', '=', property_id)])
        return request.render('property.property_view_template', {'property': property_obj})
