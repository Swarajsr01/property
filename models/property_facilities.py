# -*- coding: utf-8 -*-
"""Handle facilities of property"""

from odoo import models, fields


class PropertyFacilities(models.Model):
    """Properties facilities model"""
    _name = "property.facilities"
    _description = "Property Facilities"
    _rec_name = "facility_name"

    facility_name = fields.Char("Facility")
    facility_color = fields.Integer("Color")
