# -*- coding: utf-8 -*-
"""report wizard"""

from odoo import models, fields
from odoo.exceptions import ValidationError
from xlsxwriter.utility import xl_col_to_name
import io, base64, tempfile
import json
import xlsxwriter
from odoo.tools import json_default


class RentLeaseReportWizard(models.TransientModel):
    """wizard for report"""
    _name = "rent.lease.report.wizard"
    _description = "Rent or lease report wizard"

    state = fields.Selection(
        [('draft', 'Draft'), ('approve', 'Approve'), ('confirmed', 'Confirmed'), ('returned', 'Returned'),
         ('closed', 'Closed'), ('expired', 'Expired')])
    tenant_ids = fields.Many2many('res.partner', relation='rent_lease_report_tenant_rel',
                                  column1='rent_lease_report_id', column2='tenant_id', string='Tenant')
    owner_ids = fields.Many2many('res.partner', relation='rent_lease_report_owner_rel',
                                 column1='rent_lease_report_id', column2='owner_id', string='Owner')
    type = fields.Selection([('rent', 'Rent'), ('lease', 'Lease')], string='Type')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    property_ids = fields.Many2many('property.management', string='Properties')

    def action_print_report_pdf(self):
        """action for pdf report printing"""
        data = self.data_getting_for_report()
        return self.env.ref('property.action_rent_report').report_action(self, data=data)

    def data_getting_for_report(self):
        """function to generate data"""
        query = """SELECT rent.sequence,tenant.name AS tenant,property.name AS property,owner.name AS owner,rent.type,
        order_line.property_amount AS amount,rent.state FROM rent_order_lines AS order_line
        INNER JOIN property_management AS property ON order_line.property_name_id = property.id
        INNER JOIN rent_management AS rent ON order_line.order_id = rent.id  
        INNER JOIN res_partner AS owner ON property.owner_id = owner.id 
        INNER JOIN res_partner AS tenant ON rent.tenant_id = tenant.id 
        WHERE rent.company_id = %s"""
        params = [self.env.user.company_id.id]
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise ValidationError("To date cannot be earlier than from date.")
            else:
                query += """ AND rent.start_date >= %s"""
                query += """ AND rent.end_date <= %s"""
                params += [self.from_date, self.to_date]
        elif self.from_date and not self.to_date:
            query += """ AND rent.start_date >= %s"""
            params.append(self.from_date)
        elif not self.from_date and self.to_date:
            query += """ AND rent.end_date <= %s"""
            params.append(self.to_date)
        if self.state:
            query += """ AND rent.state = %s"""
            params.append(self.state)
        if self.type:
            query += """ AND rent.type = %s"""
            params.append(self.type)
        if self.property_ids:
            query += """ AND property.id IN %s"""
            params.append(tuple(self.property_ids.mapped('id')))
        if self.owner_ids:
            query += """ AND owner.id IN %s"""
            params.append(tuple(self.owner_ids.mapped('id')))
        if self.tenant_ids:
            query += """ AND tenant.id IN %s"""
            params.append(tuple(self.tenant_ids.mapped('id')))
        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()
        if not report:
            raise ValidationError("No record found based on your condition")
        for record in report:
            record['type'] = dict(self.fields_get()['type']['selection']).get(record.get('type'))
            record['state'] = dict(self.fields_get()['state']['selection']).get(record.get('state'))
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'report': report
        }
        return data

    def action_report_excel(self):
        """action for Excel report"""
        data = self.data_getting_for_report()
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'rent.lease.report.wizard',
                     'options': json.dumps(data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Rent Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """function for generate excel"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        amount_format = workbook.add_format({'font_size': '10px', 'align': 'right'})
        company_info_format = workbook.add_format({'font_size': '7px', 'align': 'center', 'bold': True})

        sheet.merge_range('C2:J3', 'RENT/LEASE REPORT', head)
        company = self.env.company
        logo_data = company.logo
        company_info = f"""{company.name}
        {company.street or ''} {company.street2 or ''}
        {company.city or ''}, {company.state_id.name or ''} {company.zip or ''}
        {company.country_id.name or ''}"""
        image_data = base64.b64decode(logo_data)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp_file.write(image_data)
        tmp_file.close()
        sheet.merge_range('K2:N6', ' ', cell_format)
        sheet.insert_image('L2', tmp_file.name, {'x_scale': 0.3, 'y_scale': 0.3})
        sheet.write('K2', company_info, company_info_format)
        if data['from_date']:
            sheet.merge_range(f'A{5}:B{5}', "From Date : ", txt)
            sheet.merge_range(f'C{5}:D{5}', data['from_date'], txt)
        if data['to_date']:
            sheet.merge_range(f'A{6}:B{6}', "To Date : ", txt)
            sheet.merge_range(f'C{6}:D{6}', data['to_date'], txt)
        head = ['Sequence', 'Tenant', 'Property', 'Owner', 'Amount', 'Type', 'State']
        a = 0
        for head_name in head:
            sheet.merge_range(f'{xl_col_to_name(a)}{8}:{xl_col_to_name(a + 1)}{8}', head_name, cell_format)
            a += 2
        i = 9
        for line in data['report']:
            sheet.merge_range(f'A{i}:B{i}', line.get('sequence'), txt)
            sheet.merge_range(f'C{i}:D{i}', line.get('tenant'), txt)
            sheet.merge_range(f'E{i}:F{i}', line.get('property'), txt)
            sheet.merge_range(f'G{i}:H{i}', line.get('owner'), txt)
            sheet.merge_range(f'I{i}:J{i}', f"${line.get('amount')}", amount_format)
            sheet.merge_range(f'K{i}:L{i}', line.get('type'), txt)
            sheet.merge_range(f'M{i}:N{i}', line.get('state'), txt)
            i += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
