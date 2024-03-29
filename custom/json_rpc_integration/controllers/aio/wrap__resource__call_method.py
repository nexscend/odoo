# -*- coding: utf-8 -*-

import logging
import base64
from odoo import http, SUPERUSER_ID, models, fields
from odoo.http import request
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED
from .response import error_response, success_response, success_message_response
from odoo.modules.registry import Registry
from odoo.tests import get_db_name

_logger = logging.getLogger(__name__)

registry = Registry(get_db_name())


def wrap__resource__call_method(modelname, method, id=None, **jdata):
    # Try call method of object
    _logger.info("Try call method of object: modelname == %s; obj_id == %s; method == %s; len(jdata) == %s" \
                 % (modelname, id, method, len(jdata)))
    _logger.debug("jdata == %s" % jdata)
    cr, uid = registry.cursor(), request.session.uid
    cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    Model = request.env(cr, uid)[modelname]
    # Model = request.env[modelname]
    try:
        # Validate method of model
        Method_of_model = getattr(Model.browse(id), method, None)
        if callable(Method_of_model):
            # Execute method of object
            res = Method_of_model(**jdata)
            cr.commit()
            cr.close()
            if isinstance(res, bytes) and res.startswith(b'%PDF-'):
                res = base64.encodebytes(res).decode('utf-8')
            elif isinstance(res, models.Model):
                try:
                    res = (res._name, res.ids)
                except:
                    res = (res._name, [])
            if not res:
                res = {'message': 'Execute Method Successfully.'}
            # if not isinstance(res,bool):
            return {
                "isFullFilled": True,
                "statusCode": 200,
                "data": res
            }
        else:
            return error_response(status=501, odoo_error="Method Doesn't Exist in this MODEL.")
    except Exception as e:
        if not cr.closed:
            cr.close()
        return error_response(status=409, odoo_error=str(e))
