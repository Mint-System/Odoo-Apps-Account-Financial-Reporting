Setup taxes:

- Install `l10n_ch_reports`
- Switch to "CH Company"
- In the account settings click "Refresh tax mappings"
- For account tag "+221" change external id to "__custom__.l10n_ch_tag_plus_220"
- Import the file "acccount.tax-OSS.csv"
- Update the currency rates

Create invoices:

- Create an invoice for a partner "Sweden" with country "Sweden"
- Add a product and apply the tax "25.0% SE VAT"
- Copy the invoice twice
- In the last invoice change partner with country "Estonia"
- set tax to "22.0% EE VAT (inkl.)"

Generate report:

- Open the "Account OSS Report" menu
- Mark all entries and select "Action > Download OSS Report"
