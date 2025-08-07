import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountGeneralLedger(models.AbstractModel):
    _inherit = "account.general.ledger.report.handler"

    def _get_query_amls(self, report, options, expanded_account_ids, offset=0, limit=None):
        """
        Extending `query` by extra `contra_accounts` field
        and return it to General Ledger Report.
        """
        result = super()._get_query_amls(report, options, expanded_account_ids, offset, limit)
        full_query = result[0]
        all_params = result[1]
        if full_query:
            account_move_line_ref = "account_move_line.ref,"
            if full_query.find(account_move_line_ref) != -1:
                query_with_contra_accounts = full_query.replace(
                    account_move_line_ref, "account_move_line.contra_accounts,\n" + account_move_line_ref
                )
            else:
                query_with_contra_accounts = full_query

            _logger.info("Query with Contra Accounts: %s", query_with_contra_accounts)

            return (query_with_contra_accounts, all_params)
        return result
