import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountOSSReport(models.TransientModel):
    _name = "account.oss.report"
    _description = "Account OSS Report"

    _id = fields.Integer("ID", readonly=True)
    country_code = fields.Char(readonly=True)
    tax_type = fields.Selection(
        [("standard", "Standard"), ("reduced", "Reduced"), ("exempt", "Exempt")],
        readonly=True,
    )
    tax_rate = fields.Float(readonly=True)
    base_amount = fields.Monetary(readonly=True)
    tax_amount = fields.Monetary(readonly=True)
    currency_id = fields.Many2one("res.currency", readonly=True)

    @api.model
    def _get_report_data(self):
        tag_id = self.env.ref("l10n_eu_oss.tag_oss")
        account_move_line_ids = self.env["account.move.line"].search(
            [
                "&",
                ("tax_ids", "!=", False),
                ("parent_state", "=", "posted"),
                ("tax_tag_ids", "in", tag_id.id),
            ]
        )
        # account_move_line_ids = account_move_line_ids.filtered(lambda l: tag_id in l.)
        report_data = []
        for account_move_line in account_move_line_ids:
            report_data.append(
                {
                    "_id": account_move_line.id,
                    "country_code": account_move_line.name,
                }
            )
        self.sudo().create(report_data)

    @api.model
    def refresh_report(self, context=None):
        self.search([]).sudo().unlink()
        self._get_report_data()
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
