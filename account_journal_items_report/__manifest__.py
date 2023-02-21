{
    "name": "Account Journal Items Report",
    "summary": """
        Report journal items grouped by account.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Accounting",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account", "account_move_line_contra_accounts"],
    "data": ["report/account_move_line_report.xml", "security/ir.model.access.csv"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
