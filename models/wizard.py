from odoo import fields, models, api


class WizardModel(models.TransientModel):
    _name = 'estate.property.update'
    _description = "Updates bedrooms and Living Area"

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()

    def update_field(self):
        active_id = self.env.context.get('active_id')
        rec = self.env['estate.property'].browse(int(active_id))
        bedrooms = self.bedrooms
        living_area = self.living_area
        for record in rec:
            record.bedrooms = bedrooms
            record.living_area = living_area

