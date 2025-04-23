# -*- coding: utf-8 -*-
"""website for property management"""

from odoo import http, Command
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class PropertyRentController(http.Controller):
    @route(['/property'], type="http", auth="user", website=True)
    def form_of_rent_order(self):
        """open the form of website rent"""
        return request.render("property.properties_website_template")

    @route('/property/rent/order', type='json', auth='user')
    def website_form_submit(self, **post):
        """create rent order based on form details"""
        property_ids = post.get('property_ids')
        type = post.get('type')
        from_date = post.get('from_date')
        to_date = post.get('to_date')
        total_days = post.get('total_days')
        if property_ids:
            existing_orders = request.env['rent.management'].sudo().search([
                ('tenant_id', '=', request.env.user.partner_id.id),
                ('type', '=', type),
                ('start_date', '=', from_date),
                ('end_date', '=', to_date),
                ('total_days', '=', total_days),
            ])
            if existing_orders:
                for order in existing_orders:
                    selected_property_ids = set(property_ids)
                    existing_property_ids = set(order.order_line_ids.mapped('property_name_id').ids)
                    if selected_property_ids == existing_property_ids:
                        return {
                            'message': 'You already submitted this rent order with the same properties and date range.'
                        }
            order_lines = []
            for property in property_ids:
                property_id = request.env['property.management'].browse(property)
                if post.get('type') == 'rent':
                    amount = property_id.rent_amount
                else:
                    amount = property_id.lease_amount
                order_lines.append({
                    'property_id': property_id.id,
                    'quantity': total_days,
                    'amount': amount,
                })
            record = {
                'tenant_id': request.env.user.partner_id.id,
                'type': type,
                'start_date': from_date,
                'end_date': to_date,
                'payment_due_date': to_date,
                'total_days': total_days,
                'order_line_ids': [
                    Command.create(
                        {"property_name_id": line["property_id"], "property_qty": line["quantity"],
                         "property_amount": line["amount"],
                         "property_total_amount": float(line["quantity"]) * line["amount"]})
                    for line in order_lines
                ],
            }
            request.env['rent.management'].sudo().create(record)
        return {'redirect_url': '/property/thank_you'}

    @http.route('/get/property/amount', type='json', auth='user')
    def get_property_amount(self, **kwargs):
        """get and return property amount"""
        property_rec = request.env['property.management'].sudo().browse(int(kwargs['property_id']))
        if kwargs['type'] == 'rent':
            return {'response_value': property_rec.rent_amount or 0.0}
        else:
            return {'response_value': property_rec.lease_amount or 0.0}

    @http.route('/property/thank_you', type='http', auth='user', website=True)
    def thank_you(self):
        """when the user create a rent order .then redirect to the thank you page"""
        return request.render('property.thank_you_page')

class RentalPortalAccount(CustomerPortal):
    """class that use for add a feature to customer portal"""
    def _prepare_home_portal_values(self, counters):
        """add count to the template to show the menu in portal"""
        values = super()._prepare_home_portal_values(counters)
        if 'rent_lease_count' in counters:
            rental_lease_count = request.env['rent.management'].sudo().search_count(
                [('tenant_id', '=', request.env.user.partner_id.id)])
            values['rent_lease_count'] = rental_lease_count
        return values

    @http.route('/my/home/rent_orders', type='http', auth="user",
                website=True)
    def portal_rent_orders(self):
        """To search the recruitments data in the portal"""
        rent_orders = request.env['rent.management'].sudo().search([('tenant_id', '=', request.env.user.partner_id.id)],
                                                                   order='id desc')
        return request.render('property.portal_my_home_rent_list_views', {'rent_orders': rent_orders,
                                                                          'page_name': 'rent-orders'})

    @http.route('/my/home/rent_orders/rent_orders-<sequence>', type='http', auth="user", website=True)
    def rent_order_by_sequence(self, sequence):
        """give selected sequence record to template"""
        rent_order = request.env['rent.management'].sudo().search([('sequence', '=', sequence)])
        type = dict(rent_order.fields_get()['type']['selection']).get(rent_order.type)
        return request.render('property.portal_my_home_rent_views', {'rent_order': rent_order,
                                                                     'type': type,
                                                                     'page_name': 'rent-order'})

