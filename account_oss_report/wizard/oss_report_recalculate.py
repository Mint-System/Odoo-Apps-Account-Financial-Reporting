from odoo import fields, models


class OssReportRecalculate(models.TransientModel):
    _name = "oss.report.recalculate"
    _description = "Recalculate OSS report"

    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    def recalculate_oss_report(self):
        self.env["account.oss.report"].get_data(self.start_date, self.end_date)

        tree_view_id = self.env.ref(
            "account_oss_report.view_account_oss_report_tree"
        ).id

        return {
            "type": "ir.actions.act_window",
            "views": [(tree_view_id, "tree")],
            "view_mode": "tree",
            "name": "OSS Tax Report",
            "res_model": "account.oss.report",
            "domain": [],
            "context": dict(
                self.env.context, start_date=self.start_date, end_date=self.end_date
            ),
        }
