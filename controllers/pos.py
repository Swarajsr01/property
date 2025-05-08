# -*- coding: utf-8 -*-
"""pos controller for"""

from odoo import http
from odoo.http import request
import ast


class PosCategory(http.Controller):
    @http.route('/pos/get_category_settings_discount', type='json', auth='user')
    # @route('/pos/get_category_settings_discount', type="json", auth="user", methods=['POST'])
    def get_settings_categories_discount(self):
        """open the form of website rent"""
        print("123456")
        param = request.env['ir.config_parameter'].sudo()
        discount_categories = param.get_param('res.config.settings.selected_category_ids', '[]')
        discount_amount = float(param.get_param('res.config.settings.category_wise_discount_amount', '0'))
        try:
            cat_ids = ast.literal_eval(discount_categories)
        except Exception:
            cat_ids = []
        # category_data = [{'id': category.id, 'name': category.name}
        #                  for category in request.env['pos.category'].sudo().browse(cat_ids)]

        return {'category_ids': cat_ids,
                'discount_amount': discount_amount}
