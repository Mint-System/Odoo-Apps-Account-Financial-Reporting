# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Report Referrer",
    "summary": """
        Module summary.
    """,
    "author": "Mint System GmbH",
    "website": "https://www.mint-system.ch",
    "category": "Repository",
    "version": "16.0.1.0.0",
    "license": "OPL-1",
    "depends": ["account", "partner_commission"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "demo": ["demo/demo.xml"],
    "assets": {
        "web.assets_backend": [
            "account_report_referrer/static/src/css/style.css",
        ]
    },
}