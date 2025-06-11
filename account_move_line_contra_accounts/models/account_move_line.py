import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    contra_accounts = fields.Char(
        compute="_compute_contra_accounts", readonly=True, store=True
    )

    @api.depends("move_id.line_ids")
    def _compute_contra_accounts(self):
        for rec in self:
            account_codes = (
                line.account_id.code
                for line in rec.move_id.line_ids
                if line.account_id.code and line.account_id.code != rec.account_id.code
            )
            rec.contra_accounts = ", ".join(list(sorted(account_codes)))
