from odoo import http
from odoo.http import request


class OtpController(http.Controller):
    # @http.route('/api/otp/get/', type="json", auth="none", cors="*", csrf=False)
    # def api_otp_get(self, phone_number: str, **kwargs):
    #     return {"otp_code": 1234, "phone_number": phone_number, "otp_type": "register"}

    @http.route('/api/otp/verify', type="json", auth="none", cors="*", csrf=False)
    def api_otp_get(self, phone_number: str, otp_code: str, **kwargs):
        if otp_code == 1234:
            request.session.authenticate(request.session.db, login=phone_number, password=str(otp_code))
            return {"success": True}
        return {"success": False}
