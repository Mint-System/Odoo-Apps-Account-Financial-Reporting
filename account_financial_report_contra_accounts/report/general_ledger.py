from odoo import _, api, models
import logging
_logger = logging.getLogger(__name__)


class GeneralLedgerReport(models.AbstractModel):
    _inherit = 'report.account_financial_report.general_ledger'

    @api.model
    def _get_move_line_data(self, move_line):
        res = super()._get_move_line_data(move_line)
        res['contra_accounts'] = move_line['contra_accounts']
        return res

    def _get_ml_fields(self):
        return super()._get_ml_fields() + ['contra_accounts']
