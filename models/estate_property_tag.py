from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag details"
    _order = "name desc"

    name = fields.Char(required=True)
    color = fields.Integer("Color Index")

    _sql_constraints = [
        ('unique_tag_name', 'unique (name)',
         "The Tag must be unique"),
    ]