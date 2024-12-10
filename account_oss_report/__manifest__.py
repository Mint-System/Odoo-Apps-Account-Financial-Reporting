{
    "name": "Account OSS Report",
    "summary": """
        Generate the EU VAT OSS report to upload and declare.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Accounting",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["l10n_eu_oss"],
    "data": [
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/account_oss_report_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
