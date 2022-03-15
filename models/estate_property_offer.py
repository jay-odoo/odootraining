from odoo import fields, models, api
from datetime import datetime, timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'),
                   ('refused', 'Refused'), ],
        copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property")
    create_date = fields.Date(string='Created date')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date", inverse="_inverse_date", store=True)

    @api.depends("create_date", "validity")
    def _compute_date(self):
        for record in self:
            record.date_deadline = datetime.date(datetime.today() + timedelta(days=record.validity))

    def _inverse_date(self):
        for record in self:
            print("=========================")
            print((record.date_deadline - record.create_date).days)
            record.validity = (record.date_deadline - record.create_date).days
