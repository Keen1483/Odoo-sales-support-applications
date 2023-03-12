# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BashList(models.AbstractModel):
    _name = 'report.bash_print_list.template_bash_report_tree_view'

    @api.model
    def _get_report_values(self, docids, data=data):
        print(docids)
        print(data)
