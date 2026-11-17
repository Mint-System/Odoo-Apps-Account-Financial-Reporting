---
commit_ref: 076bab3af21f95107da53dbece3ce39e1412ad2c
title: "Change titel in followup report"
author: "Janik von Rotz <login@janikvonrotz.ch>"
session_id:
action: execute
state: completed
date_completed: 2026-11-17
harness: pi
provider: mistral
model: deepseek-v4-1-flash-1017
session_id: 01a1e834-b6fa-7403-ac46-6bd5de15e079
input_tokens: 24196
output_tokens: 6008
---

# Change titel in followup report

Note: @Clanker refers to the "ai agent" (you) who is working on this prompt file.

@Clanker when working on this prompt file, make sure to:

- Read the `AGENTS.md` and `README.md` to get an understanding of the project
- Change this prompt file only
- State findings without making suggestions

## Research

I have an Odoo instance with `l10n_ch_reports` and `account_followup` installed.

Then I switch to "CH Company" and open `base.res_partner_2`. I send the reminder mail with template `	account_reports.email_template_customer_follow_up_report`. Odoo attachets a document `Acme Corporation - mahnbericht_stand_17.11.2026_ch_company.pdf`. In that document there is a title "Mahnbericht".

How can I rename the translated title from "Mahnbericht" to "Rechnungsübersicht"?

You can search the code in `./odoo` and `./enterprise`.

@Clanker When research is completed set frontmatter state to review.If you have access to session info add token count and session id. Prompt the author to verify the findings.

## Findings

### Where the title comes from

The PDF title is not a dedicated field. It is rendered from the `report_title` render value, which falls back to the translated `name` of the `account.report` record.

Render chain:

1. `res.partner._get_partner_account_report_attachment()` (`enterprise/account_reports/models/res_partner.py:57`) builds options and calls `report.export_to_pdf(options)`.
2. `account.report._get_pdf_export_html()` (`enterprise/account_reports/models/account_report.py:6303`) sets `'report_title': options.get('report_title') or self.name`.
3. The follow-up report uses the primary template `account_reports.pdf_export_main_customer_report` (`enterprise/account_reports/data/customer_reports_pdf_export_templates.xml:4`), selected in `account.followup.report.handler._custom_options_initializer()` (`enterprise/account_reports/models/account_followup_report.py:23-24`).
4. That template prints `<t t-out="report_title"/>` inside `<div class='o_title text-center'>` (`customer_reports_pdf_export_templates.xml:9`). The generic template `account_reports.pdf_export_main` does the same at `data/pdf_export_templates.xml:23`.

Because `options['report_title']` is never set for the follow-up flow (`_init_options_export` only copies it from previous options, `account_report.py:2021`), the title is `account.report` id `account_reports.followup_report`, whose `name` field is `Follow-Up Report` (`enterprise/account_reports/data/followup_report.xml:4`). `name` is `translate=True` (`account_report.py:8062`), so the German value `Mahnbericht` is used.

### Where the German string is defined

- Source record: `enterprise/account_reports/data/followup_report.xml:4` — `<field name="name">Follow-Up Report</field>`, no `noupdate`, so it is updated on module upgrade.
- Translation: `enterprise/account_reports/i18n/de.po:3238-3240`
  ```
  #: model:account.report,name:account_reports.followup_report
  msgid "Follow-Up Report"
  msgstr "Mahnbericht"
  ```
- The same German term also exists for the mail template name (`de.po:3234-3235`, `email_template_customer_follow_up_report`) and the client action (`de.po:3248-3250`, `action_account_report_followup`), but neither is used for the PDF title.
- `l10n_ch_reports` does not override the follow-up report name, title, or template (`grep` for `followup`/`follow_up` in `enterprise/l10n_ch_reports` returns nothing).

### Filename note

The filename part `mahnbericht_stand_17.11.2026_ch_company.pdf` comes from `account.report.get_default_report_filename()` (`account_report.py:4702-4727`), which uses `sections_source.name.lower().replace(' ', '_')` plus the period string and company name. It is derived from the same `name` field, so renaming the report name also renames the file.

### Ways to rename the title

1. Per database, no code: open the report record in the UI (Settings → Technical → Reports, or the report's own settings) and change the translated value of `name` for language `de`. Since `name` is translatable, the German value can be set directly on `account.report` id `account_reports.followup_report`.
2. Per database, data record: write the German translation, e.g. via `account.report` browse on `account_reports.followup_report` with `with_context(lang='de_CH')` and `name = 'Rechnungsübersicht'`.
3. Module-level: override `account_reports.followup_report`'s `name` field in a custom module's XML data (`<record id="account_reports.followup_report" model="account.report">` with `<field name="name">Rechnungsübersicht</field>`), or ship an updated `de.po` with `msgstr "Rechnungsübersicht"` for `msgid "Follow-Up Report"`.
4. Title-only, keeping the report name: override `_get_pdf_export_html()` or set `options['report_title']` in a custom handler inheriting `account.followup.report.handler`, e.g. in `_custom_options_initializer()` or via `_init_options_export()`. This changes only the PDF header, not the filename.

Note that options 1-3 change both the PDF title and the filename, and also the report name shown in the UI.

@Clanker If author confirms findings set frontmatter state to completed, otherwise to aborted. Update date, harness, provider and model. If you have access to session info update token count.
