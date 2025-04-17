# -*- coding: utf-8 -*-
"""Model for handle rent orders line"""

from odoo import models, fields


class RentOrderLines(models.Model):
    """Model for rent order line"""
    _name = "rent.order.lines"
    _description = "Rent Order Lines"
    _rec_name = "order_id"

    order_id = fields.Many2one('rent.management', string='Order', ondelete='cascade')
    property_name_id = fields.Many2one('property.management', string='Properties')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    property_amount = fields.Monetary(string='Amount', readonly=False)
    property_qty = fields.Float("Quantity", readonly=False)
    property_total_amount = fields.Monetary(string='Total Amount')
    linked_line_ids = fields.Many2many(
        string="Linked invoice lines",
        comodel_name='account.move.line',
        relation='rent_order_lines_invoice_rel',
        column1='rent_order_line_id',
        column2='rent_invoice_line_id',
        copy=False)

    def _prepare_rent_invoice_line(self):
        """ To generate invoice line """
        self.ensure_one()
        res = {
            'name': self.property_name_id.name,
            'quantity': self.order_id.total_days,
            'price_unit': self.property_amount,
        }
        return res










