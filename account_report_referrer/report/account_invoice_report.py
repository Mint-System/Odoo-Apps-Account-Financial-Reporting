from odoo import api, fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    referrer_id = fields.Many2one("res.partner", string="Referrer", readonly=True)

    @api.model
    def _select(self):
        select_query = super()._select()
        additional_select = SQL(",\nmove.referrer_id AS referrer_id")
        return SQL("%s%s", select_query, additional_select)
