from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class ReportAccountMoveLine(models.AbstractModel):
    _name = 'report.account_journal_items_report.account_move_line'
    _description = 'Journal items grouped by account'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move.line'].browse(docids) 

        # Group by account
        domain = [('id', 'in', docids)]
        fields = ['date', 'name', 'journal_id', 'move_id', 'contra_accounts', 'debit', 'credit', 'balance', 'cumulated_balance', 'currency_id']
        groupby = ['account_id']
        # orderby = 'date'
        docs_grouped = docs.read_group(domain=domain, fields=fields, groupby=groupby)
        docs_data = []
        for doc in docs_grouped:
            account_id = doc['account_id'][0]
            acccount = self.env['account.account'].browse(account_id)
            domain = doc['__domain']
            lines = docs.search_read(domain, fields)
            docs_data.append({
                'id': acccount.id,
                'code': acccount.code,
                'name': acccount.name,
                'lines': lines
            })
        # _logger.warning([docs_data])
        
        return {
            'doc_ids': docids,
            'doc_model': 'account.move.line',
            'docs': docs,
            'docs_data': docs_data,
            'from_date': min(docs.mapped('date')),
            'until_date': max(docs.mapped('date')), 
        }