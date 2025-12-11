from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def filter_timesheet_report_lines(self):
        return self.filtered(
            lambda line: line.is_service
            and (line.product_id.service_policy == "delivered_timesheet")
            and not (line.is_expense or line.is_downpayment)
        )
