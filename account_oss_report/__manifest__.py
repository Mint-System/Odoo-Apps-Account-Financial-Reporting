{
    "name": "Account OSS Report",
    "summary": """
        Create OSS tax report for CH.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Accounting",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["account", "l10n_eu_oss"],
    "data": [
        "views/account_oss_report.xml",
        "wizard/oss_report_recalculate.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
