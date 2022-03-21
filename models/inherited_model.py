from odoo import fields, models, api


class InheritedModel(models.Model):
    _inherit = "res.users"
    _description = 'Description'

    property_ids = fields.One2many("estate.property", "user_id", string="Property Ids")
