import base64
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    country_id = fields.Many2one(
        "res.country", related="partner_id.country_id", store=True
    )

    def download_oss_report(self):
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

        account_move_line_ids = self.read_group(
            domain=[("id", "in", self.ids)],
            fields=[
                "tax_ids",
                "tax_base_amount",
                "credit",
                "country_id",
                "currency_id",
            ],
            groupby=["country_id"],
        )

        csv = """
#v1.0
#ve1.1.0
Land des Verbrauchs,Umsatzsteuertyp,Umsatzsteuersatz,Nettobetrag,Umsatzsteuerbetrag
"""
        currenty_eur = self.env.ref("base.EUR")

        for group_line in account_move_line_ids:
            domain = group_line.get("__domain") or domain
            rec = self.search(domain, limit=1)

            country_code = rec.country_id.code
            tax_type = "STANDARD"
            tax_rate = rec.tax_line_id.amount

            # Convert to EUR
            base_amount = rec.currency_id.with_context(
                date=fields.Date.today()
            ).compute(group_line["tax_base_amount"], currenty_eur)
            tax_amount = rec.currency_id.with_context(date=fields.Date.today()).compute(
                group_line["credit"], currenty_eur
            )

            # Format
            tax_rate = f"{tax_rate:.2f}"
            base_amount = f"{base_amount:.2f}"
            tax_amount = f"{tax_amount:.2f}"

            csv += f"{country_code},{tax_type},{tax_rate},{base_amount},{tax_amount}\n"

        # Write the file
        attachment = self.env.ref("account_oss_report.account_oss_report")
        attachment.write({"datas": base64.b64encode(csv.encode())})

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "new",
        }
