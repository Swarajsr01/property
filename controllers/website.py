# -*- coding: utf-8 -*-
"""webiste for property management"""

from odoo import http, Command
from odoo.http import request, route


class PropertyRentController(http.Controller):
    @route(['/property'], type="http", auth="user", website=True)
    def form_of_rent_order(self, **kwargs):
        """open the form of website rent"""
        return request.render("property.properties_website_template")

    @route('/property/rent/order', type='http', auth='user', website=True, methods=['POST'])
    def website_form_submit(self, **post):
        print("test")
        """create rent order based on form details"""
        property_ids = []
        properties = post.get('property')
        print(properties)
        if properties:
            for property_id in properties:
                if property_id != ',':
                    property_ids.append(int(property_id))
            order_lines = []
            for property in property_ids:
                property_id = request.env['property.management'].browse(property)
                if post.get('type') == 'rent':
                    amount = property_id.rent_amount
                else:
                    amount = property_id.lease_amount
                order_lines.append({
                    'property_id': property_id.name,
                    'quantity': post.get('total_days'),
                    'amount': amount,
                })
            record = {
                'tenant_id': request.env.user.partner_id.id,
                'type': post.get('type'),
                'start_date': post.get('from_date'),
                'end_date': post.get('to_date'),
                'payment_due_date': post.get('to_date'),
                'total_days': post.get('total_days'),
                'order_line_ids': [
                    Command.create(
                        {"property_name_id": line["property_id"], "property_qty": line["quantity"],
                         "property_amount": line["amount"],
                         "property_total_amount": float(line["quantity"]) * line["amount"]})
                    for line in order_lines
                ],
            }
            request.env['rent.management'].sudo().create(record)
        else:
            print("no property for create rent order")
        return request.render("property.thank_you_page")

    @http.route('/get/property/amount', type='json', auth='user', website=True)
    def get_property_amount(self, **kwargs):
        """get and return property amount"""
        property_rec = request.env['property.management'].sudo().browse(int(kwargs['property_id']))
        if kwargs['type'] == 'rent':
            return {'response_value': property_rec.rent_amount or 0.0}
        else:
            return {'response_value': property_rec.lease_amount or 0.0}



    # addtional button .usig for checking
    @route(['/property/rent'], type="http", auth='user', website=True)
    def display_property_test(self, **post):
        print("ertyui")
        # return request.render("property.web_form_template")
