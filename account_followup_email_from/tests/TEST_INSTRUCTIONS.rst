Setup:

- Install Module "Account Followup Email From".
- Goto Settings > Technical > Parameters > System Parameters
- Add a new system parameter "account_followup_email_from.email_from".
- Set value to a valid email address.

Create Invoice and trigger Follow-up

- Create new Invoice.
- Go to Accounting > Customers > Follow-up Reports.
- Create new Follow-up with Action "Email".
- Check if Email sent has sender address in accordance with the system parameter you set.
- If Email sending failed e.g. due to testing you can check Email in Settings > Technical > Emails.
