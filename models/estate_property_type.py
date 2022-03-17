from odoo import fields, models, api, _


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type details"
    _order = "name desc"

    name = fields.Char(required=True)
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    property_ids = fields.One2many("estate.property", "property_type_id")

    @api.depends('offer_ids')
    def _compute_offer(self):
        for rec in self:
            rec.offer_count = len([id_count for id_count in rec.offer_ids])

    def action_offers(self):
        related_offer_ids = self.env['estate.property.offer'].search([
            ('property_type_id', '=', self.id),
        ]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': _('Offers'),
            'res_model': 'estate.property.offer',
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', related_offer_ids)],
        }

    _sql_constraints = [
        ('unique_type_name', 'unique (name)',
         "The Type must be unique"),
    ]
