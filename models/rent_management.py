# -*- coding: utf-8 -*-
"""To handle rent management  and functions"""

from odoo import models, fields, api, _, Command
from odoo.exceptions import ValidationError


class RentManagement(models.Model):
    """Rent management model for control record related to rent orders for properties"""
    _name = "rent.management"
    _description = "Rent Management"
    _rec_name = "sequence"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char('Sequence', default=lambda self: _('Sequence'), readonly=True, copy=False)
    state = fields.Selection(
        [('draft', 'Draft'), ('approve', 'Approve'), ('confirmed', 'Confirmed'), ('returned', 'Returned'),
         ('closed', 'Closed'), ('expired', 'Expired')], default='draft')
    tenant_id = fields.Many2one('res.partner', string='Tenant', required=True)
    property_id = fields.Many2one('property.management', required=False)
    type = fields.Selection([('rent', 'Rent'), ('lease', 'Lease')], string='Type',
                            required=True, default='rent')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company, readonly=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    payment_due_date = fields.Date('Payment Due Date', required=True, readonly=False)
    total_days = fields.Integer('Total Days')
    total_amount = fields.Monetary('Total Amount')
    final_amount = fields.Monetary(string='Final Amount', currency_field='currency_id',
                                   compute='_compute_final_amount', copy=True)
    order_line_ids = fields.One2many('rent.order.lines', 'order_id', string='Order', copy=True)
    invoice_count = fields.Integer("invoice", compute="_compute_paid_amount", default=0)
    payment_state = fields.Selection(selection=[('draft', 'Draft'), ('not_paid', 'Not Paid'), ('paid', 'Paid'),
                                                ('partial', 'Partial')], string="Payment Status", store=True)
    paid_amount = fields.Monetary("Paid Amount", compute='_compute_paid_amount', store=True)
    due_amount = fields.Monetary("due Amount", compute='_compute_paid_amount', store=True)
    invoice_visibility = fields.Boolean("Invoice visible", compute='_compute_invoice_visibility', store=True,
                                        default=True)

    @api.depends('order_line_ids.linked_line_ids.move_id.state', 'order_line_ids', 'state')
    def _compute_invoice_visibility(self):
        """fully invoiced then invisible invoice button from form view"""
        for rec in self:
            ordered_qty = sum(line.property_qty for line in rec.order_line_ids)
            invoiced_qty = (sum(line.quantity for line in
                                rec.order_line_ids.linked_line_ids.filtered(lambda l: l.move_id.state == 'posted')))
            if rec.state in ['confirmed', 'closed', 'returned', 'expired']:
                if rec.invoice_count > 0 and invoiced_qty >= ordered_qty:
                    rec.invoice_visibility = True
                else:
                    rec.invoice_visibility = False
            else:
                rec.invoice_visibility = True

    @api.depends('order_line_ids.property_total_amount', 'total_days')
    def _compute_final_amount(self):
        """Calculate the sum property line total amount"""
        for record in self:
            record.final_amount = sum(line.property_total_amount for line in record.order_line_ids)

    @api.depends('order_line_ids.linked_line_ids.move_id.payment_state',
                 'order_line_ids.linked_line_ids.move_id.amount_residual')
    def _compute_paid_amount(self):
        """Calculate count of invoices for smart button """
        for rec in self:
            rec.invoice_count = len(rec.order_line_ids.mapped("linked_line_ids.move_id"))
            posted_invoice = rec.order_line_ids.mapped("linked_line_ids.move_id").filtered(
                lambda l: l.state == 'posted')
            states = posted_invoice.mapped("payment_state")
            if posted_invoice:
                amount_residual = sum(invoice.amount_residual for invoice in posted_invoice)
                amount_total = sum(invoice.amount_total for invoice in posted_invoice)
                rec.due_amount = amount_residual
                rec.paid_amount = amount_total - amount_residual
            if len(posted_invoice) > 0:
                if all(state == "paid" for state in states):
                    rec.payment_state = 'paid'
                elif all(state == "not_paid" for state in states):
                    rec.payment_state = 'not_paid'
                else:
                    rec.payment_state = 'partial'

    @api.onchange('end_date')
    def _onchange_end_date(self):
        """autofill payment due date when changes end date"""
        self.payment_due_date = self.end_date

    @api.onchange('start_date', 'end_date')
    def _onchange_start_date(self):
        """Calculate total days"""
        if self.start_date and self.end_date:
            self.total_days = int((self.end_date - self.start_date).days)

    @api.onchange('type')
    def _onchange_type(self):
        """Fetch line property amount."""
        for line in self.order_line_ids:
            if self.type == 'rent':
                line.property_amount = line.property_name_id.rent_amount
            else:
                line.property_amount = line.property_name_id.lease_amount

    @api.onchange('order_line_ids', 'total_days')
    def _onchange_order_line_ids(self):
        """Calculate line property total amount"""
        total_days = self.total_days
        for line in self.order_line_ids:
            if line.property_name_id:
                if line.property_qty != total_days:
                    line.property_qty = total_days
                if line.property_amount == 0:
                    if self.type == 'rent':
                        line.property_amount = line.property_name_id.rent_amount
                    else:
                        line.property_amount = line.property_name_id.lease_amount
                else:
                    if self.type == 'rent':
                        line.property_name_id.rent_amount = line.property_amount
                    else:
                        line.property_name_id.lease_amount = line.property_amount
                line.property_total_amount = line.property_qty * line.property_amount

    @api.onchange('order_line_ids')
    def _onchange_order_line_ids_exist(self):
        """Check existing property or not"""
        exist_rent_list = []
        for line in self.order_line_ids:
            if line.property_name_id.id in exist_rent_list:
                raise ValidationError(_('The property should be different'))
            exist_rent_list.append(line.property_name_id.id)

    @api.model_create_multi
    def create(self, vals_list):
        """Create sequence"""
        for vals in vals_list:
            vals['sequence'] = (self.env['ir.sequence'].next_by_code('rent.sequence'))
        return super(RentManagement, self).create(vals_list)

    def action_rent_invoiced(self):
        """Rent smart button view"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'list, form',
            'views': [(False, 'list'), (False, 'form')],
            'res_model': 'account.move',
            'domain': [('partner_id', '=', self.tenant_id.id),
                       ("move_type", "=", "out_invoice"),
                       ("ref", "=", self.sequence)],
            'target': "current",
        }

    def action_confirm(self):
        """Confirm button"""
        if not self.message_attachment_count > 0:
            raise ValidationError(_("You want to upload related file"))
        else:
            if self.env.user.has_group('property.group_property_manager'):
                self.write({
                    'state': "confirmed"
                })
                if self.type == "rent":
                    self.order_line_ids.property_name_id.write({
                        'state': "rent"
                    })
                else:
                    self.order_line_ids.property_name_id.write({
                        'state': "leased"
                    })
                template = self.env.ref('property.mail_template_rent_order_confirm')
                self.message_post_with_source(template, subject="Rent order confirmed", message_type='comment',
                                              subtype_xmlid="mail.mt_comment")
            else:
                self.write({
                    'state': "approve"
                })

    def action_returned(self):
        """Returned button"""
        if not self.message_attachment_count > 0:
            raise ValidationError(_("You want to upload related file"))
        else:
            self.write({
                'state': "returned"
            })
            self.order_line_ids.property_name_id.write({
                'state': "draft"
            })

    def action_closed(self):
        """Closed button"""
        if not self.message_attachment_count > 0:
            raise ValidationError(_("You want to upload related file"))
        else:
            self.write({
                'state': "closed"
            })
            self.order_line_ids.property_name_id.write({
                'state': "draft"
            })
            template = self.env.ref('property.mail_template_rent_order_closed')
            self.message_post_with_source(template, subject="Rent order closed", message_type='comment',
                                          subtype_xmlid="mail.mt_comment")

    def action_expired(self):
        """Expired button"""
        if not self.message_attachment_count > 0:
            raise ValidationError(_("You want to upload related file"))
        else:
            self.write({
                'state': "expired"
            })
            template = self.env.ref('property.mail_template_rent_order_expired')
            self.message_post_with_source(template, subject="Rent order expired", message_type='comment',
                                          subtype_xmlid="mail.mt_comment")

    def action_reset_draft(self):
        """Reset draft button"""
        self.write({
            'state': "draft"
        })
        self.order_line_ids.property_name_id.write({
            'state': "draft"
        })

    def action_create_rent_invoice(self):
        """Invoice button for create invoice for rent order"""
        self.ensure_one()
        invoice_obj = self.env["account.move"]
        draft_invoice = self.order_line_ids.mapped("linked_line_ids.move_id").filtered(lambda l: l.state == 'draft')
        posted_invoice = self.order_line_ids.mapped("linked_line_ids.move_id").filtered(lambda l: l.state == 'posted')
        invoice_vals = self._prepare_rent_invoice()
        if not posted_invoice:
            invoice_line_vals = [Command.create(line._prepare_rent_invoice_line()) for line in self.order_line_ids]
            if not invoice_line_vals:
                raise ValidationError(_("Nothing to invoice."))
            invoice = self._prepare_invoice(draft_invoice, invoice_vals, invoice_obj, invoice_line_vals)
        else:
            order_quantities = [
                {"name": line.property_name_id.name, "quantity": line.property_qty, "price_unit": line.property_amount}
                for line in self.order_line_ids
            ]
            for order in order_quantities:
                linked_lines_ids = self.order_line_ids.linked_line_ids.filtered(
                    lambda l: l.name == order['name'] and l.move_id.state == 'posted')
                invoiced = sum(line.quantity for line in linked_lines_ids)
                order['quantity'] -= invoiced
            order_quantities = [line for line in order_quantities if line["quantity"] > 0]
            if order_quantities:
                invoice_line_vals = [
                    Command.create(
                        {"name": line["name"], "quantity": line["quantity"], "price_unit": line["price_unit"]})
                    for line in order_quantities
                ]
                invoice = self._prepare_invoice(draft_invoice, invoice_vals, invoice_obj, invoice_line_vals)
            else:
                raise ValidationError("Nothing to invoice. All quantity is invoiced")
        return {
            "name": _("Rent Invoice"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": invoice.id,
            "target": "current",
        }

    def _prepare_rent_invoice(self):
        """ To fetch record details for invoice """
        self.ensure_one()
        values = {
            'move_type': 'out_invoice',
            'partner_id': self.tenant_id.id,
            'invoice_origin': self.sequence,
            'ref': self.sequence,
            'invoice_line_ids': [],
        }
        return values

    def _prepare_invoice(self, draft_invoice, invoice_vals, invoice_obj, invoice_line_vals):
        """To generate invoice for rent """
        if not draft_invoice:
            invoice_vals["invoice_line_ids"] += invoice_line_vals
            invoice = invoice_obj.create(invoice_vals)
        else:
            draft_invoice.write({"invoice_line_ids": [Command.clear()] + invoice_line_vals})
            invoice = draft_invoice
            self.message_post(body=_("Draft invoice updated!"))
        for order_line in self.order_line_ids:
            for invoice_line in invoice.invoice_line_ids:
                if order_line.property_name_id.name == invoice_line.name:
                    order_line.write({"linked_line_ids": [Command.link(invoice_line.id)]})
        return invoice

    def action_cron_rent_expiry(self):
        """ To  check if any record due date is current date and if any remaining amount to pay.
        Then send mail to the corresponding Tenant """
        today = fields.Date.today()
        expired_records = self.search(
            [('state', 'not in', ('expired', 'draft')), ('payment_due_date', '=', today)])
        for rec in expired_records:
            if rec.paid_amount < rec.final_amount:
                template = self.env.ref('property.mail_template_rent_order_expired_follow_ups')
                template.send_mail(rec.id, force_send=True)
                rec.message_post_with_source(template, subject="Rent order expired follow ups",
                                             message_type='comment', subtype_xmlid="mail.mt_comment")
            rec.state = 'expired'