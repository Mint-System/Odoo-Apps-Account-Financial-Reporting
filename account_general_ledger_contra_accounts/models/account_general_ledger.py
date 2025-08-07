import re
import logging

from odoo import models

_logger = logging.getLogger(__name__)

def add_contra_accounts_line(
    query,
    target='account_move_line.ref',
    new_column='account_move_line.contra_accounts,'):
    pattern = rf"^(.*{re.escape(target)}.*,\s*)$"
    
    def replacer(match):
        return f"{match.group(1)}\n{new_column}"

    return re.sub(pattern, replacer, query, flags=re.MULTILINE)


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
        _logger.warning("Full Query: %s", full_query)
        
        if full_query:
            query_with_contra_accounts = add_contra_accounts_line(full_query)
        #     account_move_line_refs = "account_move_line.ref"
        #     if full_query.find(account_move_line_ref) != -1:
        #         query_with_contra_accounts = full_query.replace(
        #             account_move_line_ref, "account_move_line.contra_accounts,\n" + account_move_line_ref
        #         )
        

            _logger.info("Query with Contra Accounts: %s", query_with_contra_accounts)

            return (query_with_contra_accounts, all_params)
        return result
