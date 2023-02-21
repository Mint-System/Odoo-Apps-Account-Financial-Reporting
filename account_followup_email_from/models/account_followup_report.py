from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
import ast


class AccountFollowupReport(models.AbstractModel):
    _inherit = 'account.followup.report'

    @api.model
    def send_email(self, options):
        """
        #OVERWRITE: Replace method with option to pass email from arg
        """
        partner = self.env['res.partner'].browse(options.get('partner_id'))
        non_blocked_amls = partner.unreconciled_aml_ids.filtered(lambda aml: not aml.blocked)
        if not non_blocked_amls:
            return True
        non_printed_invoices = partner.unpaid_invoices.filtered(lambda inv: not inv.message_main_attachment_id)
        if non_printed_invoices and partner.followup_level.join_invoices:
            raise UserError(_('You are trying to send a followup report to a partner for which you didn\'t print all the invoices ({})').format(" ".join(non_printed_invoices.mapped('name'))))
        invoice_partner = self.env['res.partner'].browse(partner.address_get(['invoice'])['invoice'])
        email = invoice_partner.email
        if email and email.strip():
            self = self.with_context(lang=partner.lang or self.env.user.lang)
            # When printing we need te replace the \n of the summary by <br /> tags
            body_html = self.with_context(print_mode=True, mail=True).get_html(options)
            body_html = body_html.replace('o_account_reports_edit_summary_pencil', 'o_account_reports_edit_summary_pencil d-none')
            start_index = body_html.find('<span>', body_html.find('<div class="o_account_reports_summary">'))
            end_index = start_index > -1 and body_html.find('</span>', start_index) or -1
            if end_index > -1:
                replaced_msg = body_html[start_index:end_index].replace('\n', '')
                body_html = body_html[:start_index] + replaced_msg + body_html[end_index:]
            kwargs = {
                'partner_ids': [invoice_partner.id],
                'body': body_html,
                'subject': self._get_report_manager(options).email_subject,
                'subtype_id': self.env.ref('mail.mt_note').id,
                'model_description': _('payment reminder'),
                'email_layout_xmlid': 'mail.mail_notification_light',
                'attachment_ids': partner.followup_level.join_invoices and partner.unpaid_invoices.message_main_attachment_id.ids or [],
            }
            email_from = self.env['ir.config_parameter'].sudo().get_param('account_followup_email_from.email_from', '')
            if email_from and email_from.strip():
                kwargs['email_from'] = email_from
            partner.with_context(mail_post_autofollow=True, lang=partner.lang or self.env.user.lang).message_post(**kwargs)
            return True
        raise UserError(_('Could not send mail to partner %s because it does not have any email address defined', partner.display_name))
