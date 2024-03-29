from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.models.res_partner import SignupError


class AuthController(http.Controller):
    @http.route('/api/auth/setup-password', type="json", auth="user", csrf=False, cors="*")
    def api_auth_setup_password(self, email, new_password, confirm_password, **kwargs):
        user_id = request.env['res.users'].sudo().search(domain=[('login', '=', email)], limit=1)
        if new_password != confirm_password:
            return {"message": "password doesn't match."}
        # current_user = request.env.user
        user_id.sudo()._set_to_password(new_password=new_password)
        return {"message": "password setup successfully."}

    @http.route('/api/auth/change-password', type="json", auth="user", csrf=False, cors="*")
    def api_auth_change_password(self, current_password, new_password, confirm_password):
        if new_password != confirm_password:
            return {"message": "password doesn't match."}
        result = request.env.user.change_password(old_passwd=current_password, new_passwd=new_password)
        return {"message": result}

    @http.route('/api/auth/forgot-password', type="json", auth="none", csrf=False, cors="*")
    def api_auth_forgot_password(self, email: str, new_password, **kwargs):
        user_id = request.env['res.users'].sudo().search(domain=[('login', '=', email)], limit=1)
        if user_id:
            # TODO: create a OTP
            otp_code = 1234
            user_id.sudo()._set_to_password(new_password=new_password)
            return {"message": "Password Update.", "password": new_password}
        return {"message": "Please Signup."}

    @http.route('/api/auth/register', type="json", auth="public", csrf=False, cors="*")
    def api_auth_register(self, email: str, name, **kwargs):
        # TODO: create a OTP
        otp_code = 1234
        values = {
            "login": email,
            "password": otp_code,
            "name": name,
        }
        try:
            request.env['res.users'].sudo()._signup_create_user(values)
        except SignupError as e:
            return {"message": str(e)}
        return {"message": "Register Success.", "user_id": email, "password": otp_code}

    @http.route('/api/auth/login', type="json", auth="none", csrf=False, cors="*")
    def api_auth_login(self, login: str, password: str, **kwargs):
        request.session.authenticate(request.session.db, login=login, password=password)
        user = request.env.user
        partner = user.partner_id
        return {
            "message": "Login Success.",
            "data": {
                "user": {
                    "login":user.login,
                    "id": user.id,
                    "name": user.name,
                },
                "partner": {
                    "id": partner.id,
                    "name": partner.name
                }
            }
        }
