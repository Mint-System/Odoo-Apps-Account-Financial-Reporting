import logging
from odoo import models, api, _
_logger = logging.getLogger(__name__)


class AccountGeneralLedger(models.AbstractModel):
    _inherit = 'account.general.ledger.report.handler'

    @api.model
    def _get_columns_name(self, options):
        columns_names = super()._get_columns_name(options)
        columns_names.insert(3, {'name': _('Contra Accounts')})
        return columns_names

    def _get_query_amls_select_clause(self):
        return '''
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
            full_rec.name                           AS full_rec_name
        '''

    def _get_query_amls(self, report, options, expanded_account_ids, offset=0, limit=None):
        result = super()._get_query_amls(report, options, expanded_account_ids, offset, limit)
        return result

    @api.model
    def _get_account_title_line(self, options, account, amount_currency, debit, credit, balance, has_lines):
        res = super()._get_account_title_line(options, account, amount_currency, debit, credit, balance, has_lines)
        res['colspan'] = 5
        return res

    @api.model
    def _get_initial_balance_line(self, options, account, amount_currency, debit, credit, balance):
        res = super()._get_initial_balance_line(options, account, amount_currency, debit, credit, balance)
        res['colspan'] = 5
        return res

    @api.model
    def _get_aml_line(self, options, account, aml, cumulated_balance):
        if aml['payment_id']:
            caret_type = 'account.payment'
        else:
            caret_type = 'account.move'

        columns = [
            {'name': self.format_report_date(aml['date']), 'class': 'date'},
            {'name': self._format_aml_name(aml['name'], aml['ref']), 'class': 'o_account_report_line_ellipsis'},
            {'name': aml['contra_accounts'], 'class': 'o_account_move_line_contra_accounts'},
            {'name': aml['partner_name'], 'class': 'o_account_report_line_ellipsis'},
            {'name': self.format_value(aml['debit'], blank_if_zero=True), 'class': 'number'},
            {'name': self.format_value(aml['credit'], blank_if_zero=True), 'class': 'number'},
            {'name': self.format_value(cumulated_balance), 'class': 'number'},
        ]
        if self.user_has_groups('base.group_multi_currency'):
            if (aml['currency_id'] and aml['currency_id'] != account.company_id.currency_id.id) or account.currency_id:
                currency = self.env['res.currency'].browse(aml['currency_id'])
            else:
                currency = False
            columns.insert(4, {'name': currency and aml['amount_currency'] and self.format_value(aml['amount_currency'], currency=currency, blank_if_zero=True) or '', 'class': 'number'})
        return {
            'id': aml['id'],
            'caret_options': caret_type,
            'parent_id': 'account_%d' % aml['account_id'],
            'name': aml['move_name'],
            'columns': columns,
            'level': 2,
        }

    @api.model
    def _get_account_total_line(self, options, account, amount_currency, debit, credit, balance):
        res = super()._get_account_total_line(options, account, amount_currency, debit, credit, balance)
        res['colspan'] = 5
        return res

    @api.model
    def _get_total_line(self, options, debit, credit, balance):
        res = super()._get_total_line(options, debit, credit, balance)
        res['colspan'] = self.user_has_groups('base.group_multi_currency') and 6 or 5
        return res
