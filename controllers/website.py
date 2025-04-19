# -*- coding: utf-8 -*-
"""webiste for property management"""

from odoo import http
from odoo.http import request, Controller, route
import re


class PropertyRentController(http.Controller):
    @route(['/property'], type="http", auth="user", website=True)
    def form_of_rent_order(self, **kwargs):
        """open the form of website rent"""
        return request.render("property.properties_website_template")



    @route('/property/rent/order', type='http', auth='user', website=True, methods=['POST'])
    def website_form_submit(self, **post):
        print("1234567890987654")
        print(post)
        # request.env['custom.web.form.booking'].sudo().create({
        #     'name': post.get('name'),
        #     'phone': post.get('phone'),
        #     'email': post.get('email'),
        # })
        # return request.redirect('/property/rent')






    # addtional button .usig for checking

    @route(['/property/rent'], type="http", auth='user', website=True)
    def display_property_test(self, **post):
        print("ertyui")
        return request.render("property.web_form_template")



