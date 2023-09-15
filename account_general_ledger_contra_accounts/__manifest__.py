{
    "name": "Account General Ledger Contra Accounts",
    "summary": """
        Add contra accounts to general ledger.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Accounting",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account_reports", "account_move_line_contra_accounts"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "data": ["data/general_ledger.xml"],
}
