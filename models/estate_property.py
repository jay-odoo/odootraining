from odoo import fields, models, _, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Details"
    _order = "id desc"

    name = fields.Char(required=True, default="Unknown")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    description = fields.Text()
    postcode = fields.Char(required=True, default="1000")
    city = fields.Char(required=True, default="Brussels")
    date_availability = fields.Date("Date Availability",
                                    default=lambda self: datetime.date(datetime.today() + timedelta(days=90)),
                                    copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True, store=True)
    best_price = fields.Float(compute='_compute_price', store=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute='_compute_area', store=True)
    sold_status = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new'
    )
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('canceled', 'Canceled')],
        default='new',
        compute="_compute_state"
    )

    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_price(self):
        for record in self:
            if record.offer_ids.mapped('price'):
                record.best_price = max(record.offer_ids.mapped('price'))

    @api.depends("offer_ids", "sold_status")
    def _compute_state(self):
        for rec in self:
            if rec.offer_ids:
                for offer in rec.offer_ids:
                    if offer.status == 'accepted':
                        if rec.sold_status == "sold":
                            rec.state = 'sold'
                            return
                        else:
                            rec.state = 'offer accepted'
                            return
                    else:
                        rec.state = 'offer received'
                        return
            elif rec.sold_status == "sold":
                rec.state = 'sold'
                return
            else:
                rec.state = 'new'
                return

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold_action(self):
        for record in self:
            if record.sold_status == "new":
                record.sold_status = "sold"
            elif record.sold_status == "sold":
                raise UserError("Sold Property can not be sold again")
            else:
                raise UserError("Canceled Property can not be sold")
            return True

    def sold_action_cancel(self):
        for rec in self:
            if rec.sold_status == "new":
                rec.sold_status = "canceled"
            elif rec.sold_status == "sold":
                raise UserError("Sold Property can not be cancelled")
            else:
                raise UserError("Property already canceled")
            return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for rec in self:
            if float_compare(rec.selling_price, (rec.expected_price * 0.9), 2) < 0:
                raise ValidationError("Selling price must be 90% of expected price")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0.0)',
         "The expected Price can be positive value only."),
        ('check_selling_price', 'CHECK(selling_price >= 0.0)',
         "The selling Price can be positive value only."),
    ]
