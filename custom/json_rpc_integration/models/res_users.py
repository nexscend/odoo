from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _set_to_password(self, new_password: str):
        self.flush_recordset(['password'])
        self.env.cr.execute(
            'UPDATE res_users SET password=%s WHERE id=%s',
            (new_password, self.id,)
        )
        self.invalidate_recordset(['password'])

