import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class AccountGeneralLedger(models.AbstractModel):
    _inherit = "account.general.ledger"

    @api.model
    def _get_columns_name(self, options):
        columns_names = super()._get_columns_name(options)
        columns_names.insert(1, {"name": _("Account Code")})
        columns_names.insert(4, {"name": _("Contra Accounts")})
        columns_names.insert(5, {"name": _("VAT Code")})
        return columns_names

    def _get_query_amls_select_clause(self):
        return """
            account_move_line.id,
            account_move_line.date,
            account_move_line.date_maturity,
            account_move_line.name,
            account_move_line.ref,
            account_move_line.contra_accounts,
            account_move_line.company_id,
            account_move_line.account_id,
            account_move_line.payment_id,
            account_move_line.partner_id,
            account_move_line.currency_id,
            account_move_line.amount_currency,
            ROUND(account_move_line.debit * currency_table.rate, currency_table.precision)   AS debit,
            ROUND(account_move_line.credit * currency_table.rate, currency_table.precision)  AS credit,
            ROUND(account_move_line.balance * currency_table.rate, currency_table.precision) AS balance,
            account_move_line.move_name,
            company.currency_id                     AS company_currency_id,
            partner.name                            AS partner_name,
            move.move_type                          AS move_type,
            account.code                            AS account_code,
            account.name                            AS account_name,
            journal.code                            AS journal_code,
            journal.name                            AS journal_name,
            full_rec.name                           AS full_rec_name,
            (
            SELECT STRING_AGG(tax.description, ', ')
            FROM account_move_line_account_tax_rel aml_tax
            LEFT JOIN account_tax tax ON tax.id = aml_tax.account_tax_id
            WHERE aml_tax.account_move_line_id = account_move_line.id
            ) AS vat_code
        """


    @api.model
    def _get_account_title_line(
        self, options, account, amount_currency, debit, credit, balance, has_lines
    ):
        res = super()._get_account_title_line(
            options, account, amount_currency, debit, credit, balance, has_lines
        )
        res["colspan"] = 7
        return res

    @api.model
    def _get_initial_balance_line(
        self, options, account, amount_currency, debit, credit, balance
    ):
        res = super()._get_initial_balance_line(
            options, account, amount_currency, debit, credit, balance
        )
        res["colspan"] = 7
        return res

    @api.model
    def _get_aml_line(self, options, account, aml, cumulated_balance):
        if aml["payment_id"]:
            caret_type = "account.payment"
        else:
            caret_type = "account.move"

        columns = [
            {
                "name": aml["account_code"],
                "class": "o_account_move_line_account_code",
            },
            {"name": self.format_report_date(aml["date"]), "class": "date"},
            {
                "name": self._format_aml_name(aml["name"], aml["ref"]),
                "class": "o_account_report_line_ellipsis",
            },
            {
                "name": aml["contra_accounts"].split(", ")[0] if aml["contra_accounts"] else "",
                "class": "o_account_move_line_contra_accounts",
            },
            {
                "name": aml["vat_code"] if aml["vat_code"] else "",
                "class": "o_account_move_line_vat_code",
            },
            {"name": aml["partner_name"], "class": "o_account_report_line_ellipsis"},
            {
                "name": self.format_value(aml["debit"], blank_if_zero=True),
                "class": "number",
            },
            {
                "name": self.format_value(aml["credit"], blank_if_zero=True),
                "class": "number",
            },
            {"name": self.format_value(cumulated_balance), "class": "number"},
        ]
        if self.user_has_groups("base.group_multi_currency"):
            if (
                aml["currency_id"]
                and aml["currency_id"] != account.company_id.currency_id.id
            ) or account.currency_id:
                currency = self.env["res.currency"].browse(aml["currency_id"])
            else:
                currency = False
            columns.insert(
                6,
                {
                    "name": currency
                    and aml["amount_currency"]
                    and self.format_value(
                        aml["amount_currency"], currency=currency, blank_if_zero=True
                    )
                    or "",
                    "class": "number",
                },
            )
        return {
            "id": aml["id"],
            "caret_options": caret_type,
            "parent_id": "account_%d" % aml["account_id"],
            "name": aml["move_name"],
            "columns": columns,
            "level": 2,
        }

    @api.model
    def _get_account_total_line(
        self, options, account, amount_currency, debit, credit, balance
    ):
        res = super()._get_account_total_line(
            options, account, amount_currency, debit, credit, balance
        )
        res["colspan"] = 7
        return res

    @api.model
    def _get_total_line(self, options, debit, credit, balance):
        res = super()._get_total_line(options, debit, credit, balance)
        res["colspan"] = self.user_has_groups("base.group_multi_currency") and 8 or 7
        return res
