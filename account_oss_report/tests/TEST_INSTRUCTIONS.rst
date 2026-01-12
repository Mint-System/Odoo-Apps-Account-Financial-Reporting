Setup taxes:

- Install `l10n_ch_reports`
- Switch to "CH Company"
- In the account settings click "Refresh tax mappings"
- For account tag "+221" change external id to "__custom__.l10n_ch_tag_plus_220"
- Import the file "acccount.tax-OSS.csv"
- Update the currency rates

Create invoices:

- Create an invoice for partner "Sweden"
- Add a product with price 100 CHF and apply the tax "25.0% SE VAT"
- Confirm and copy the invoice
- Change product price to 150
- Copy the invoice again
- Change partner to "Estonia"
- Set tax to "22.0% EE VAT (inkl.)"

Generate report:

- Open the "Account OSS Report" menu
- Mark all entries and select "Action > Download OSS Report"
- Check calculation is correct:

SE: (100+150)*1.0445 and (100+150)*1.0445*0.25
EE: (150-150*0.22/(1+0.22))*1.0445 and (150-150*0.22/(1+0.22))*1.0445*0.22

Generate credit:

- Create credit for "Estoania"
- Add product with price 50 CHF
- Confirm the credit
- Generate the OSS report
- Ensure that the
