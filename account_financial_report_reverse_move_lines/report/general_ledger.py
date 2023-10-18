import logging

from odoo import models

_logger = logging.getLogger(__name__)


class GeneralLedgerReport(models.AbstractModel):
    _inherit = "report.account_financial_report.general_ledger"

    def _get_list_grouped_item(
        self, data, account, rec_after_date_to_ids, hide_account_at_0, rounding
    ):
        account, list_grouped = super()._get_list_grouped_item(
            data, account, rec_after_date_to_ids, hide_account_at_0, rounding
        )
        for group_item in list_grouped:
            group_item["move_lines"].reverse()
        return account, list_grouped
