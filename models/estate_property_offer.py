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
            record.validity = (record.date_deadline - record.create_date).days

    def status_change_accepted(self):
        for rec in self:
            if not rec.status:
                rec.status = 'accepted'
        if self.status == 'accepted':
            self.property_id.selling_price = self.price
            self.property_id.partner_id = self.partner_id
        return True

    def status_change_refused(self):
        for rec in self:
            if not rec.status:
                rec.status = 'refused'
        return True

    # @api.onchange("status")
    # def _onchange_status(self):
    #     print("==================")
    #     # print(self.property_id.offer_ids.mapped('price'))
    #     print(self.price)
    #     print(self.property_id.selling_price)
    #     print("==================")
    #     if self.status == 'accepted':
    #         self.property_id.selling_price = self.price
    #     print("==================")
    #     # print(self.property_id.offer_ids.mapped('price'))
    #     print(self.property_id.selling_price)
    #     print("==================")
