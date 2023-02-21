from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    contra_accounts = fields.Char(compute='_compute_contra_accounts', readonly='1', store=True)

    @api.depends('move_id.line_ids')
    def _compute_contra_accounts(self):
        for rec in self:
            account_codes = rec.move_id.line_ids.mapped('account_id.code')
            account_codes = list(filter(lambda c: c != rec.account_id.code, account_codes))
            account_codes.sort()
            # _logger.warning([rec, account_codes])
            rec.contra_accounts = ', '.join(account_codes)
