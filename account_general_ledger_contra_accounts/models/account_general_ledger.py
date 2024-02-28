import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountGeneralLedger(models.AbstractModel):
    _inherit = "account.general.ledger.report.handler"

    def _get_query_amls(
        self, report, options, expanded_account_ids, offset=0, limit=None
    ):
        """
        Extending `query` by extra `contra_accounts` field
        and return it to General Ledger Report.
        """
        result = super()._get_query_amls(
            report, options, expanded_account_ids, offset, limit
        )
        full_query = result[0]
        all_params = result[1]
        if full_query:
            insert_index = full_query.find("account_move_line.ref,") + len(
                "account_move_line.ref,"
            )
            query_with_contra_accounts = (
                full_query[:insert_index]
                + "account_move_line.contra_accounts,\n"
                + full_query[insert_index:]
            )
            return (query_with_contra_accounts, all_params)
        return result
