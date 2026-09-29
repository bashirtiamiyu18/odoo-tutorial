from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one(
        "estate.property",
        required=True,
        ondelete="cascade",
    )
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ]
    )