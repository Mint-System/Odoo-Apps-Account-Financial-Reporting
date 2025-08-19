import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountGeneralLedger(models.AbstractModel):
    _inherit = "account.general.ledger.report.handler"

    def _get_aml_values(self, report, options, expanded_account_ids, offset=0, limit=None):
        aml_results, has_more = super()._get_aml_values(report, options, expanded_account_ids, offset, limit)
        for key1, level1 in aml_results.items():
            for key2, level2 in level1.items():
                for key, line in level2.items():
                    if line["ref"]:
                        line["communication"] = line["name"]
        return aml_results, has_more
