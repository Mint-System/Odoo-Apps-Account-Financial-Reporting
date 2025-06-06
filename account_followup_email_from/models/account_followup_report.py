import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class AccountFollowupReport(models.AbstractModel):
    _inherit = "account.followup.report"

    @api.model
    def _send_email(self, options):
        """
        #OVERWRITE: Replace method with option to pass email from arg
        Send by email the followup to the customer's followup contacts
        """
        partner = self.env['res.partner'].browse(options.get('partner_id'))
        sent_at_least_once = False
        for to_send_partner in self._get_email_recipients(options):
            email = to_send_partner.email
            if email and email.strip():
                self = self.with_context(lang=partner.lang or self.env.user.lang)
                body_html = self.with_context(mail=True).get_followup_report_html(options)

                attachment_ids = options.get('attachment_ids', partner._get_invoices_to_print(options).message_main_attachment_id.ids)
                # If the follow-up was executed manually, the author_id will be set to the ID of the current logged-in user.
                # Otherwise, if the follow-up is automatic, the author_id will be the followup responsible or OdooBot.
                author_id = options.get('author_id', partner._get_followup_responsible().partner_id.id)

                email_from_parameter = (
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("account_followup_email_from.email_from", "")
                )

                if email_from_parameter and email_from_parameter.strip():
                    email_from = email_from_parameter
                else:
                    email_from = self._get_email_from(options)

                partner.with_context(mail_post_autofollow=True, mail_notify_author=True, lang=partner.lang or self.env.user.lang).message_post(
                    partner_ids=[to_send_partner.id],
                    author_id=author_id,
                    #email_from=self._get_email_from(options),
                    email_from=email_from,
                    body=body_html,
                    subject=self._get_email_subject(options),
                    reply_to=self._get_email_reply_to(options),
                    model_description=_('payment reminder'),
                    email_layout_xmlid='mail.mail_notification_light',
                    attachment_ids=attachment_ids,
                    subtype_id=self.env['ir.model.data']._xmlid_to_res_id('mail.mt_note'),
                )
                sent_at_least_once = True
        if not sent_at_least_once:
            raise UserError(_("You are trying to send an Email, but no follow-up contact has any email address set for customer '%s'", partner.name))
