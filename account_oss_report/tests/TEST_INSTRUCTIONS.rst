Setup taxes:

- Install `l10n_ch_reports`
- Switch to "CH Company"
- In the account settings click "Refresh tax mappings"
- Enable EUR currency
- Set currency rate to 1.0445

Create invoices:

- Create an invoice for partner "Sweden"
- Add a product with price 100 CHF and apply the tax "25.0% SE USt-IdNr."
- Confirm and copy the invoice
- Change product price to 150
- Copy the invoice again
- Change partner to "Estonia"
- Set tax to "24.0% EE USt-IdNr." and confirm

Generate report:

- Open the "Account OSS Report" menu
- Mark all entries and select "Action > Download OSS Report"
- Check calculation is correct:

SE: 250*1.0445=261.125 and 250*1.0445*0.25=65.28125
EE: 150*1.0445=156.675  and 150*1.0445*0.24=37.602

Generate credit:

- Create credit for "Estoania"
- Add product with price 50 CHF and apply the tax "24.0% EE USt-IdNr."
- Confirm the credit
- Generate the OSS report
- Ensure that the amount is deducted.
