from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    def _get_columns_name(self, options):
        res = super(AccountFollowupReport , self)._get_columns_name(options)
        for index, item in enumerate(res):
            if item.get('name') and item.get('name') == _('Communication'):
                res.pop(index)
        return res

    def _get_lines(self, options, line_id=None):
        res = super(AccountFollowupReport , self)._get_lines(options, line_id)
        _logger.warning(res)
        for index, item in enumerate(res):
            columns = item.get('columns')      
            if columns:
                columns.pop(3)
                res[index]['columns'] = columns
        _logger.warning(res)
        return res
