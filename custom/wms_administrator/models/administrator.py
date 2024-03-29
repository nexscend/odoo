# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model_create_multi
    def create(self, vals_list):
        # 999/0
        configs = super().create(vals_list)
        # for config in configs:
        #     if config.twitter_api_key or config.twitter_api_secret or config.twitter_screen_name:
        #         config._check_twitter_authorization()
        return configs