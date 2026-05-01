# -*- coding: utf-8 -*-
from odoo import models


class AccountReport(models.Model):
    _inherit = 'account.report'


    def get_default_report_filename(self, options, extension):
        """The default to be used for the file when downloading pdf,xlsx,..."""
        self.ensure_one()

        sections_source_id = options['sections_source_id']
        if sections_source_id != self.id:
            sections_source = self.env['account.report'].browse(sections_source_id)
        else:
            sections_source = self

        return f"{sections_source.name.replace(' ', '_')}.{extension}"