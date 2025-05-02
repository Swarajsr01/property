# -*- coding: utf-8 -*-
"""add new feature to product template model"""

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_quality = fields.Selection(selection=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'),
                                                  ('4', '4'), ('5', '5')], default='0', string="Product_rate")
