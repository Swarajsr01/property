# -*- coding: utf-8 -*-
"""Model for handle properties"""

from odoo import models, fields, api


class PropertyManagement(models.Model):
    """Manage properties record"""
    _name = "property.management"
    _description = "Property Management"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection([('draft', 'Draft'), ('rent', 'Rent'), ('leased', 'Leased'), ('sold', 'Sold')],
                             default='draft', string='Stage', tracking=True)
    name = fields.Char('Name', required=True, tracking=True)
    image = fields.Image('Image')
    street = fields.Char('Street')
    street2 = fields.Char('Street 2')
    city = fields.Char('City ')
    zip = fields.Char('ZIP')
    state_id = fields.Many2one('res.country.state', 'State')
    country_id = fields.Many2one('res.country', 'Country')
    description = fields.Html('Description')
    build_date = fields.Date('Built date')
    sold_or_not = fields.Boolean('Can be sold', tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company, readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    lease_amount = fields.Monetary('Lease Amount', tracking=True)
    rent_amount = fields.Monetary('Rent', tracking=True)
    owner_id = fields.Many2one('res.partner', 'Owner', tracking=True, required=True)
    order_count = fields.Integer(compute='_compute_order_count')
    facility_ids = fields.Many2many('property.facilities', string='Facilities')
    active = fields.Boolean(default=True)

    @api.depends('owner_id.partner_rent_ids')
    def _compute_order_count(self):
        """ To count the rent order for current property"""
        for record in self:
            record.order_count = self.env['rent.management'].search_count(
                [('order_line_ids.property_name_id', '=', record.id)])

    def action_rent_order(self):
        """smart button view"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'list,form',
            'res_model': 'rent.management',
            'domain': [('order_line_ids.property_name_id', '=', self.id)],
        }

    def unlink(self):
        """remove unlinked record from other related rent model """
        for record in self:
            self.env['rent.management'].search([]).mapped("order_line_ids").filtered(
                lambda l: l.property_name_id == record).unlink()
            self.env['rent.management'].search([]).filtered(lambda l: not l.order_line_ids).unlink()
        return super(PropertyManagement, self).unlink()

