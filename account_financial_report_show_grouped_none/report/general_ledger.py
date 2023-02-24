from odoo import _, api, models
import logging
_logger = logging.getLogger(__name__)


class GeneralLedgerReport(models.AbstractModel):
    _inherit = 'report.account_financial_report.general_ledger'

    def _create_account_not_show_item(
        self, account, acc_id, gen_led_data, rec_after_date_to_ids, grouped_by
    ):
        move_lines = []
        for prt_id in gen_led_data[acc_id].keys():
            if not isinstance(prt_id, int):
                account.update({prt_id: gen_led_data[acc_id][prt_id]})
            elif isinstance(gen_led_data[acc_id][prt_id], dict):
                if 'entry' in gen_led_data[acc_id][prt_id].keys():
                    move_lines += [gen_led_data[acc_id][prt_id]]        
        move_lines = sorted(move_lines, key=lambda k: (k["date"]))
        move_lines = self._recalculate_cumul_balance(
            move_lines,
            gen_led_data[acc_id]["init_bal"]["balance"],
            rec_after_date_to_ids,
        )
        
        account.update({"move_lines": move_lines, grouped_by: False})
        return account