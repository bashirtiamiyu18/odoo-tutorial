from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char(string="Post code")
    date_availability = fields.Date(copy=False, string="Available From", default=(fields.Date.today() + relativedelta(months=3)))
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    cancel = fields.Char()
    sold = fields.Char()
    garage = fields.Boolean()
    garden = fields.Boolean()
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    garden_orientation = fields.Selection(selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West"),])
    state = fields.Selection(selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")], default="new")

    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.partner", string="Salesperson", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id",  string="Offer")

    @api.depends("living_area", "garden_area")    
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices, default=0)

    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([("north", "North"), ("south", "Sourth"), ("east", "East"), ("west", "West"),])


    
    
    def action_cancel(self):
            for prop in self:
                if prop.state == 'sold':
                    raise UserError("Sold properties cannot be canceled.") 
                prop.state = 'canceled'
            return True
    
    def action_sold(self):
            for prop in self:
                if prop.state == 'canceled':
                    raise UserError("Canceled properties cannot be sold.")
                prop.state = 'sold'
            return True
    

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    







            