# -*- coding: utf-8 -*-
"""webiste for property management"""

from odoo import http, Command
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
# from odoo.addons.portal.controllers import portal


class PropertyRentController(http.Controller):
    @route(['/property'], type="http", auth="user", website=True)
    def form_of_rent_order(self, **kwargs):
        """open the form of website rent"""
        return request.render("property.properties_website_template")

    @route('/property/rent/order', type='json', auth='user', website=True)
    def website_form_submit(self, **post):
        """create rent order based on form details"""
        property_ids = post.get('property_ids')
        if property_ids:
            order_lines = []
            for property in property_ids:
                property_id = request.env['property.management'].browse(property)
                if post.get('type') == 'rent':
                    amount = property_id.rent_amount
                else:
                    amount = property_id.lease_amount
                order_lines.append({
                    'property_id': property_id.id,
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
        return {'redirect_url': '/property/thank_you'}

    @http.route('/get/property/amount', type='json', auth='user', website=True)
    def get_property_amount(self, **kwargs):
        """get and return property amount"""
        property_rec = request.env['property.management'].sudo().browse(int(kwargs['property_id']))
        if kwargs['type'] == 'rent':
            return {'response_value': property_rec.rent_amount or 0.0}
        else:
            return {'response_value': property_rec.lease_amount or 0.0}

    @http.route('/property/thank_you', type='http', auth='public', website=True)
    def thank_you(self, **kwargs):
        return request.render('property.thank_you_page')

class RentalPortalAccount(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'rental_lease_count' in counters:
            rental_lease_count = request.env['rent.management'].sudo().search_count(
                [('tenant_id', '=', request.env.user.partner_id.id)])
            values['rental_lease_count'] = rental_lease_count
        return values

    @http.route(['/my/rent_orders', '/my/rent_orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_recruitment(self, search=None, search_in='All'):
        """To search the recruitments data in the portal"""
        # searchbar_inputs = {
        #     'All': {'label': 'All', 'input': 'All', 'domain': []},
        #     'Job Position': {'label': 'Job Position', 'input': 'Job Position', 'domain': [('job_id', 'like', search)]},
        #     'Status': {'label': 'Status', 'input': 'Status', 'domain': [('stage_id', 'like', search)]},
        # }
        # search_domain = searchbar_inputs[search_in]['domain']
        rent_orders = request.env['rent.management'].sudo().search([('tenant_id', '=', request.env.user.partner_id.id)],
                                                                   order='id desc')
        return request.render('property.portal_my_home_rent_views', {'rent_orders': rent_orders})
