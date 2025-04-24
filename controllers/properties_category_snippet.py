from odoo import http
from odoo.http import request, route

class WebsiteProduct(http.Controller):
    @http.route('/get_properties_categories', auth="public", type='json',
                website=True)
    def get_properties_category(self):
        """Get the website categories for the snippet."""
        properties_ids = request.env[
            'property.management'].sudo().search([], order='id desc', limit=4)
        val = []
        for property in properties_ids:
            val.append({'id': property.id,
                        'image': property.image,
                        'name': property.name,
                        'owner': property.owner_id.name,
                        'build_date': property.build_date,
                        })
        values = {
            'properties': val,
        }
        return values

    @route('/property/<property_id>', type='http', auth="user", website=True)
    def current_property_details(self, property_id):
        print(property_id)
        property_obj = request.env['property.management'].sudo().search([('id', '=', property_id)])
        print(property_obj)

        return request.render('property.property_view_template', {'property': property_obj})

