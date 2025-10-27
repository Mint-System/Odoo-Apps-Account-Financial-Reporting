import base64
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    country_id = fields.Many2one("res.country", related="partner_id.country_id", store=True)

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
        csv = """#v3.0
#ve3.3.0
"""
        # Land des Verbrauchs,Umsatzsteuertyp,Umsatzsteuersatz,"Steuerbemessungsgrundlage, Nettobetrag",Umsatzsteuerbetrag,Importmeldung
        # List countries
        for country_id in list(set(self.mapped("country_id"))):
            rate_type = 1
            country_code = country_id.code
            csv += f"{rate_type},{country_code}\n"

        # List revenue by country
        currency_eur = self.env.ref("base.EUR")

        # Use _read_group with new syntax
        account_move_line_ids = self._read_group(
            domain=[("id", "in", self.ids)],
            groupby=["country_id"],
            aggregates=["tax_base_amount:sum", "credit:sum"],
        )

        for group_line in account_move_line_ids:
            # group_line is a tuple: (country_id_value, tax_base_amount_sum, credit_sum)
            country_recordset, tax_base_amount_sum, credit_sum = group_line

            if not country_recordset:
                continue

            # Find a representative record from this group to get tax info
            rec = self.search([("id", "in", self.ids), ("country_id", "=", country_recordset.id)], limit=1)

            rate_type = 2
            country_code = country_recordset.code
            tax_type = "STANDARD"
            tax_rate = rec.tax_line_id.amount if rec.tax_line_id else 0.0

            # Convert to EUR using _convert method
            company = rec.company_id or self.env.company
            conversion_date = fields.Date.today()

            base_amount = rec.currency_id._convert(tax_base_amount_sum, currency_eur, company, conversion_date)
            tax_amount = rec.currency_id._convert(credit_sum, currency_eur, company, conversion_date)

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
