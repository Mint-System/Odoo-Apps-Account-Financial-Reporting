from odoo import api, fields, models


class AccountOSSReport(models.Model):
    _name = "account.oss.report"
    _description = "OSS Tax Report"

    country_code = fields.Char()
    tax_rate = fields.Float()
    base_amount = fields.Float()
    tax_amount = fields.Float()
    net_amount = fields.Float()
    tax_type = fields.Selection([("included", "Included"), ("excluded", "Excluded")])

    @api.model
    def _get_account_move_line_data(self, data=None, start_date=False, end_date=False):
        if data is None:
            data = []

        oss_tag = self.env.ref("account_oss_report.account_tag_oss")

        domain = [
            ("move_id.invoice_date", ">=", start_date),
            ("move_id.invoice_date", "<=", end_date),
            ("tax_ids", "!=", False),
            ("tax_tag_ids", "in", [oss_tag.id]),
        ]

        move_lines = self.env["account.move.line"].search(domain)

        grouped_lines = {}
        for line in move_lines:
            country_code = (
                line.tax_ids[0].country_id.code if line.tax_ids else "Unknown"
            )
            tax_rate = line.tax_ids[0].amount if line.tax_ids else 0.0

            tax_type = "included" if line.tax_ids[0].price_include else "excluded"

            key = (country_code, tax_rate, tax_type)
            if key not in grouped_lines:
                grouped_lines[key] = {
                    "country_code": country_code,
                    "tax_rate": tax_rate,
                    "base_amount": 0.0,
                    "tax_amount": 0.0,
                    "net_amount": 0.0,
                    "tax_type": tax_type,
                }

            move = line.move_id
            grouped_lines[key]["base_amount"] += move.amount_untaxed_signed
            grouped_lines[key]["tax_amount"] += move.amount_tax_signed
            grouped_lines[key]["net_amount"] += move.amount_total_signed

        for values in grouped_lines.values():
            data.append(values)

        return data

    @api.model
    def get_data(self, start_date=False, end_date=False):
        data = []

        data = self._get_account_move_data(data, start_date, end_date)

        self.env.cr.execute("DELETE FROM account_oss_report")

        self.create(data)
