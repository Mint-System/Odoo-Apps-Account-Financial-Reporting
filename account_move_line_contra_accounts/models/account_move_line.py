from odoo import api, fields, models


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
                if line.account_id.code != rec.account_id.code
            )

            rec.contra_accounts = ", ".join(sorted(set(account_codes)))
