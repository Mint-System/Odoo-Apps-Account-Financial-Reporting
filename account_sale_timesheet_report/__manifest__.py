{
    "name": "Account Sale Timesheet Report",
    "summary": """
        Timesheet report for invoicing.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Accounting",
    "version": "15.0.1.1.1",
    "license": "AGPL-3",
    "depends": ["account_sale_timesheet"],
    "data": [
        "report/timesheet_report.xml",
        "report/report_invoice.xml",
        "views/account_report.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
