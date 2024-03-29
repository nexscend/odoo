# -*- coding: utf-8 -*-
from odoo import http
from .aio.decorator import check_register_models
from .aio import (
    wrap__resource__call_method,
    wrap__resource__read_all,
    wrap__resource__read_one,
    wrap__resource__update_one,
    wrap__resource__create_one,
    wrap__resource__delete_one,
)


class ControllerREST(http.Controller):

    # Read all (with optional filters, offset, limit, order, exclude_fields, include_fields):
    @http.route('/api/model/<string:model>', type='json', auth='public', csrf=False, cors="*")
    @check_register_models
    def api__general_model__GET(self, model: str, model_definitions: dict, **optional: dict) -> dict:
        print("___model",model)
        return wrap__resource__read_all(
            modelname=model,
            default_domain=model_definitions['default_list_domains'],
            OUT_fields=model_definitions['list_fields'],
            **optional
        )

    @http.route('/api/model/<string:model>/<int:id>', type='json', auth='public')
    @check_register_models
    def api__general_model__id_GET(self, model: str, model_definitions: dict, id: int, **kw):
        return wrap__resource__read_one(
            modelname=model,
            id=id,
            OUT_fields=model_definitions['detail_fields']
        )

    # Create one:
    @http.route('/api/model/<string:model>/create', type='json', auth='public', csrf=False)
    @check_register_models
    def api__general_model__POST(self, model: str, model_definitions: dict, **data):
        print("____data",data)
        del data['models']
        return wrap__resource__create_one(
            modelname=model,
            default_vals=model_definitions['default_create_fields'],
            OUT_fields=model_definitions['detail_fields'],
            **data
        )

    # Update one:
    @http.route('/api/model/<string:model>/<int:id>/update', type='json', auth='public', csrf=False, cors="*")
    @check_register_models
    def api__general_model__id_PUT(self, model: str, model_definitions: dict, id: int, **data):
        del data['models']
        print("____data",data)
        return wrap__resource__update_one(
            modelname=model,
            id=id,
            **data
        )

    # Delete one:
    @http.route('/api/model/<string:model>/<int:id>/delete', type='json', auth='public', csrf=False, cors="*")
    @check_register_models
    def api__general_model__id_DELETE(self, model: str, models: str, id: int, model_definitions: dict):
        return wrap__resource__delete_one(
            modelname=model,
            id=id,
        )

    @http.route('/api/model/<string:model>/execute-kw/<string:method>', type='json', auth='public', csrf=False,
                cors="*")
    @check_register_models
    def api__general_model__method_PUT(self, model: str, method: str, model_definitions: dict, **kw):
        return wrap__resource__call_method(
            modelname=model,
            method=method,
            **kw
        )

    # Call method (with optional parameters):
    @http.route('/api/model/<string:model>/<int:id>/<string:method>', type='json', auth='public', csrf=False, cors="*")
    @check_register_models
    def api__general_model__id__method_PUT(self, model: str, id: int, method: str, model_definitions: dict, **kw):
        return wrap__resource__call_method(
            modelname=model,
            id=id,
            method=method,
            **kw
        )
