import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    country_id = fields.Many2one(
        "res.country", related="partner_id.country_id", store=True
    )
