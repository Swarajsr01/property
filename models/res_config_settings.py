# -- coding: utf-8 --
import ast
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """Extension of 'res.config.settings' for configuring delivery settings."""
    _inherit = 'res.config.settings'

    category_wise_discount_amount = fields.Float(string='Discount Amount', help='Set the discount amount')
    selected_category_ids = fields.Many2many('pos.category', 'id', string='TEST')

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        selected_category_ids = icp_sudo.get_param('res.config.settings.selected_category_ids')
        category_wise_discount_amount = icp_sudo.get_param('res.config.settings.category_wise_discount_amount')
        selected_category_ids = ast.literal_eval(selected_category_ids) if selected_category_ids else []
        res.update(
            selected_category_ids=[(6, 0, selected_category_ids)],
            category_wise_discount_amount=category_wise_discount_amount if category_wise_discount_amount else 0,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.selected_category_ids', self.selected_category_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.category_wise_discount_amount',
            self.category_wise_discount_amount)
        return res
