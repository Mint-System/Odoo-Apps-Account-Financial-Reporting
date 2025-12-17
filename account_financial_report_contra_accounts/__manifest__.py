{
    "name": "Account Financial Report Contra Accounts",
    "summary": """
        Provide contra accounts field to the OCA general ledger report.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Accounting",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account_move_line_contra_accounts", "account_financial_report"],
    "data": ["report/templates/general_ledger.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
