from odoo import fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    partner_vat = fields.Char(related='partner_id.vat', string='USt-IdNr', store=False)