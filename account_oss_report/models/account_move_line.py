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
        #v3.0
        #ve3.3.0
        1,AT
        1,BE
        1,BG
        2,AT,STANDARD,20.00,200.00,40.00
        2,AT,REDUCED,10.00,300.00,30.00
        2,BE,STANDARD,21.00,200.00,42.00
        2,BE,REDUCED,6.00,200.00,12.00
        2,BG,STANDARD,20.00,200.00,40.00
        3,AT,2021,7,100.00,23.00
        3,AT,2021,8,100.00,22.00
        3,BE,2021,7,100.00,21.00
        3,BG,2021,7,100.00,20.00
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

        csv = """#v3.0
#ve3.3.0
"""
        # Land des Verbrauchs,Umsatzsteuertyp,Umsatzsteuersatz,"Steuerbemessungsgrundlage, Nettobetrag",Umsatzsteuerbetrag,Importmeldung

        # List countries
        for country_id in list(set(self.country_id)):
            rate_type = 1
            country_code = country_id.code
            csv += f"{rate_type},{country_code}\n"

        # List revenvue by country
        currency_eur = self.env.ref("base.EUR")
        for group_line in account_move_line_ids:
            domain = group_line.get("__domain") or domain
            rec = self.search(domain, limit=1)

            rate_type = 2
            country_code = rec.country_id.code
            tax_type = "STANDARD"
            tax_rate = rec.tax_line_id.amount

            # Convert to EUR
            base_amount = rec.currency_id.with_context(
                date=fields.Date.today()
            ).compute(group_line["tax_base_amount"], currency_eur)
            tax_amount = rec.currency_id.with_context(date=fields.Date.today()).compute(
                group_line["credit"], currency_eur
            )

            # Format
            tax_rate = f"{tax_rate:.2f}"
            base_amount = f"{base_amount:.2f}"
            tax_amount = f"{tax_amount:.2f}"

            csv += f"{rate_type},{country_code},{tax_type},{tax_rate},{base_amount},{tax_amount}\n"

        # Write the file
        attachment = self.env.ref("account_oss_report.account_oss_report")
        attachment.write({"datas": base64.b64encode(csv.encode())})

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "new",
        }
