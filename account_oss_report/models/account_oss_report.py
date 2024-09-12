from odoo import api, fields, models


class AccountOssReport(models.Model):
    _name = "account.oss.report"
    _description = "OSS Tax Report"

    country_code = fields.Char()
    tax_rate = fields.Float()
    base_amount = fields.Float()
    tax_amount = fields.Float()
    net_amount = fields.Float()
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id
    )

    @api.model
    def _get_account_move_data(self, data=None, start_date=False, end_date=False):
        """
        Fetch data from account.move.line with the appropriate domain and calculations.
        """
        if data is None:
            data = []

        domain = [
            ("move_id.invoice_date", ">=", start_date),
            ("move_id.invoice_date", "<=", end_date),
            ("tax_line_id", "!=", False),
        ]
        move_lines = self.env["account.move.line"].search(domain)

        for line in move_lines:
            move = line.move_id
            base_amount = move.amount_untaxed_signed
            tax_amount = move.amount_tax_signed
            net_amount = move.amount_total_signed

            data.append(
                {
                    "country_code": line.partner_id.country_id.code
                    if line.partner_id.country_id
                    else "Unknown",
                    "tax_rate": line.tax_line_id.amount,
                    "base_amount": base_amount,
                    "tax_amount": tax_amount,
                    "net_amount": net_amount,
                    "currency_id": move.company_currency_id.id,
                }
            )

        return data

    @api.model
    def get_data(self, start_date=False, end_date=False):
        """
        Generate OSS report data for the specified date range.
        """
        data = []

        # Fetch move line data
        data = self._get_account_move_data(data, start_date, end_date)

        # Clear existing data from the report
        self.env.cr.execute("DELETE FROM account_oss_report")

        # Insert new data into the report
        self.create(data)
