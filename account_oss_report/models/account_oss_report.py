import base64
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountOSSReport(models.TransientModel):
    _name = "account.oss.report"
    _description = "Account OSS Report"

    _id = fields.Integer("ID", readonly=True)
    country_code = fields.Char(readonly=True)
    tax_type = fields.Selection(
        [("standard", "STANDARD"), ("reduced", "REDUCED"), ("exempt", "EXEMPT")],
        readonly=True,
    )
    tax_rate = fields.Float(readonly=True)
    base_amount = fields.Monetary(readonly=True)
    tax_amount = fields.Monetary(readonly=True)
    currency_id = fields.Many2one("res.currency", readonly=True)

    @api.model
    def _get_report_data(self):
        tag_id = self.env.ref("l10n_eu_oss.tag_oss")

        # Group the account move lines by country
        account_move_line_ids = self.env["account.move.line"].read_group(
            domain=[
                "&",
                ("tax_ids", "!=", False),
                ("parent_state", "=", "posted"),
                ("tax_tag_ids", "in", tag_id.id),
            ],
            fields=["tax_ids", "price_subtotal", "credit", "country_id", "currency_id"],
            groupby=["country_id"],
        )

        report_data = []
        for group_line in account_move_line_ids:
            _logger.warning(group_line)
            domain = group_line.get("__domain") or domain
            rec = self.env["account.move.line"].search(domain, limit=1)
            report_data.append(
                {
                    "tax_type": "standard",
                    "country_code": rec.country_id.code,
                    "tax_rate": rec.tax_ids[0].amount,
                    "base_amount": f"{group_line['price_subtotal']:.2f}",
                    "tax_amount": f"{group_line['credit']:.2f}",
                    "currency_id": rec.currency_id.id,
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

    @api.model
    def download_report(self, context=None):
        """
        Returns a csv file in the following format:

        ```
        #v1.0
        #ve1.1.0
        Land des Verbrauchs,Umsatzsteuertyp,Umsatzsteuersatz,'Steuerbemessungsgrundlage, Nettobetrag',Umsatzsteuerbetrag
        AT,STANDARD,20.00,200.00,40.00
        BE,STANDARD,21.00,200.00,42.00
        BG,STANDARD,20.00,200.00,40.00
        ```
        """

        report_data = self.search([])
        csv = "#v1.0\n#ve1.1.0\nLand des Verbrauchs,Umsatzsteuertyp,Umsatzsteuersatz,'Steuerbemessungsgrundlage, Nettobetrag',Umsatzsteuerbetrag\n"
        for rec in report_data:
            csv += f"{rec.country_code},{rec.tax_type},{rec.tax_rate},{rec.base_amount},{rec.tax_amount}\n"

        # Write the file
        attachment = self.env["ir.attachment"].create(
            {
                "name": "OSS Report.csv",
                "datas": base64.b64encode(csv.encode()),
                "res_model": "account.oss.report",
                "res_id": self.id,
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "new",
        }
