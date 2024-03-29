from odoo import http
from odoo.http import request


class InfoController(http.Controller):
    @http.route('/api/info/', auth="public", type="json")
    def api_info(self, **kwargs):
        return {"message": request.env.user.name}
