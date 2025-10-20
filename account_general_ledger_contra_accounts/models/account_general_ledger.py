import logging
import re

from odoo import models
from odoo.sql_db import SQL

_logger = logging.getLogger(__name__)


class AccountGeneralLedger(models.AbstractModel):
    _inherit = "account.general.ledger.report.handler"

    def _get_query_amls(self, report, options, expanded_account_ids, offset=0, limit=None) -> SQL:
        """
        Extending SQL query by extra contra_accounts field.
        """
        sql_query = super()._get_query_amls(report, options, expanded_account_ids, offset, limit)

        # Get the query string and parameters from the SQL object
        query_string = sql_query.code if hasattr(sql_query, "code") else str(sql_query)
        query_params = sql_query.params if hasattr(sql_query, "params") else ()

        # Search for the ref line and add contra_accounts after it
        pattern = r"(\n\s+MIN\(account_move_line\.ref\)\s+AS\s+ref,)"
        replacement = r"\1\n                    account_move_line.contra_accounts AS contra_accounts,"
        modified_query = re.sub(pattern, replacement, query_string, count=1)

        # Return new SQL object with same parameters
        return SQL(modified_query, *query_params)
