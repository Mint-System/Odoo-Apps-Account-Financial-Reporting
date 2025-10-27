{
    "name": "Account OSS Report",
    "summary": """
        Generate the EU VAT OSS report to upload and declare.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch/",
    "category": "Accounting",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["l10n_eu_oss"],
    "data": [
        "data/data.xml",
        "views/account_oss_report_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/res_partner_demo.xml"],
}
