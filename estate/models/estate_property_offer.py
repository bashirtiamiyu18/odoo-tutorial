from odoo import models, fields, api
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(required=True)
    date_deadline = fields.Date(required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    validity = fields.Integer(required=True)
    property_id = fields.Many2one(
        "estate.property",
        required=True,
        ondelete="cascade",)

    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline=create_date + timedelta(days=offer.validity)


    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - create_date).days
            

            
    
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ]
    )