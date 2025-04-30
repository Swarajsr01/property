from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_quality = fields.Selection(selection=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'),('4', '4'),
                                                  ('5', '5')], related='product_tmpl_id.product_quality',
                                       store=True)

    # @api.model
    # def _load_pos_data_fields(self, config_id):
    #     fields = super()._load_pos_data_fields(config_id)
    #     fields.append('product_quality')
    #     return fields