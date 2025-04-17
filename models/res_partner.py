# -*- coding: utf-8 -*-
"""To add rent notebook to res partner """
from odoo import fields, models, api


class ResPartner(models.Model):
    """Inherit model for add notebook to res partner for show related rent order for that particular res partner"""
    _inherit = "res.partner"

    partner_rent_ids = fields.Many2many('rent.management', string="Rent", compute='compute_partner_rent_ids')

    @api.depends('partner_rent_ids.sequence')
    def compute_partner_rent_ids(self):
        """To show current partner rent orders and displayed in notebook"""
        for rec in self:
            rec.partner_rent_ids = self.env['rent.management'].search([('tenant_id', '=', rec.id)])