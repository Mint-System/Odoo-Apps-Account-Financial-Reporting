from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    referrer_id = fields.Many2one("res.partner", string="Referrer", readonly=True)

    _depends = dict(models.Model._depends)
    _depends["account.move"] = _depends.get("account.move", []) + ["referrer_id"]

    @api.model
    def _select(self):
        return (
            super()._select()
            + """,
            move.referrer_id
        """
        )
