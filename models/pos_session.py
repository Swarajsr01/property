from odoo import models, fields, api
import ast

class PosSession(models.Model):
    _inherit = 'pos.session'

    category_discount_limit = fields.Float(string="Category Discount Limit", compute="_compute_category_discount")
    category_discount_category_ids = fields.Many2many('pos.category', string="Category Discount Categories")

    @api.depends('config_id')
    def _compute_category_discount(self):
        param = self.env['ir.config_parameter'].sudo()
        cat_ids_raw = param.get_param('res.config.settings.selected_category_ids', '[]')
        discount_amt = float(param.get_param('res.config.settings.category_wise_discount_amount', '0'))
        try:
            cat_ids = ast.literal_eval(cat_ids_raw)
        except Exception:
            cat_ids = []

        for session in self:
            session.category_discount_limit = discount_amt
            session.category_discount_category_ids = [(6, 0, cat_ids)]

    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        params += ['category_discount_limit', 'category_discount_category_ids']
        return params
