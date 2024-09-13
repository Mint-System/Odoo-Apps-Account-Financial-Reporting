from odoo import api, fields, models

class AccountOssReport(models.Model):
    _name = "account.oss.report"
    _description = "OSS Tax Report"

    country_code = fields.Char()
    tax_rate = fields.Float()
    base_amount = fields.Float()
    tax_amount = fields.Float()
    net_amount = fields.Float()
    # tax_type = fields.Selection()

    @api.model
    def _get_account_move_data(self, data=None, start_date=False, end_date=False):
        """
        Fetch data from account.move.line with the appropriate domain and calculations.
        """
        if data is None:
            data = []

        # Fetch the tag for "OSS" to use in the domain
        oss_tag = self.env['account.account.tag'].search([('name', '=', 'OSS')], limit=1)

        # Build the domain to filter by date, tax, and tag "OSS"
        domain = [
            ('move_id.invoice_date', '>=', start_date),
            ('move_id.invoice_date', '<=', end_date),
            ('tax_ids', '!=', False),
            ('tax_tag_ids', 'in', [oss_tag.id])
        ]

        # Fetch move lines that match the criteria
        move_lines = self.env['account.move.line'].search(domain)

        for line in move_lines:
            move = line.move_id
            base_amount = move.amount_untaxed_signed
            tax_amount = move.amount_tax_signed
            net_amount = move.amount_total_signed

            # Fetch the first tax's country code and tax rate if they exist
            if line.tax_ids:
                country_code = line.tax_ids[0].country_id.code
                tax_rate = line.tax_ids[0].amount
            else:
                country_code = 'Unknown'
                tax_rate = 0.0

            data.append({
                'country_code': country_code,
                'tax_rate': tax_rate,
                'base_amount': base_amount,
                'tax_amount': tax_amount,
                'net_amount': net_amount,
                # 'tax_type': None,
            })

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
