from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def filter_timesheet_report_lines(self):
        return self.filtered(
            lambda l: l.is_service
            and (l.product_id.service_policy == "delivered_timesheet")
            and not (l.is_expense or l.is_downpayment)
        )
