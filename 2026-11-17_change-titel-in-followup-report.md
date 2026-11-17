---
commit_ref:
title: "Change titel in followup report"
author: "Janik von Rotz <login@janikvonrotz.ch>"
session_id:
action: execute
state: draft
date_completed: YYYY-MM-DD
harness:
provider:
model:
input_tokens:
output_tokens:
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

@Clanker Add a summary here once the research has been completed.

@Clanker If author confirms findings set frontmatter state to completed, otherwise to aborted. Update date, harness, provider and model. If you have access to session info update token count.
