from odoo import http, fields, _
from odoo.http import request
from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.exceptions import AccessError, MissingError, ValidationError
import jwt
from calendar import timegm
from datetime import datetime, timedelta


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
        # current_date = datetime.now()
        current_date = datetime.utcnow().utctimetuple()
        exp = datetime.now().utcnow().replace(day=datetime.now().utcnow().day+1).utctimetuple()
        if user:
            auth_id = request.env['auth.jwt.validator'].search([('name','ilike', 'Admin')], limit=1)
            if not auth_id:
                raise ValidationError(_('JWT Validator: Not Found of AUTH JWT validator'))
            currentTimestamp =  timegm(current_date)
            expTimestamp =   timegm(exp)
            now = timegm(datetime.utcnow().utctimetuple())
            payload_data = {
                "user": request.env.user.name,
                'iat': currentTimestamp,
                'exp':  expTimestamp,
                "issuer" : auth_id.issuer,
                "audience" : auth_id.audience
                }
            token = jwt.encode(
                payload = payload_data,
                key = request.env.user.name,
                )
            auth_id.write({
                "signature_type" : 'secret',
                "secret_key" : token
                })
        return {
            "message": "Login Success.",
            "data": {
                "user": {
                    "login":user.login,
                    "id": user.id,
                    "name": user.name,
                    "token": token,
                    'iat': currentTimestamp,
                    "issuer" : auth_id.issuer,
                    "exp_time" : expTimestamp,
                    "audience" : auth_id.audience
                },
                "partner": {
                    "id": partner.id,
                    "name": partner.name
                }
            }
        }


    # @http.route('/api/auth/generate_token', type="json", auth="none", csrf=False, cors="*")
    # def api_auth_generate_token(self, login: str, password: str, **kwargs):
    #     payload = {
    #             ""
    #             }

    #     return {
    #         "message": "Login Success.",
    #         "data": {
    #             "user": {
    #                 "login":user.login,
    #                 "id": user.id,
    #                 "name": user.name,
    #             },
    #             "partner": {
    #                 "id": partner.id,
    #                 "name": partner.name
    #             }
    #         }
    #     }
