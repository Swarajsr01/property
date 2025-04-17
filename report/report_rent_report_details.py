# -*- coding: utf-8 -*-
"""model to control rent report"""

from odoo import models, api


class RentFormReport(models.AbstractModel):
    """abstract model for share data to report template"""
    _name = 'report.property.report_rent_report_details'

    @api.model
    def _get_report_values(self, docids, data):
        """give data to qweb template"""
        return ({
            'doc_ids': docids,
            'data': data,
        })