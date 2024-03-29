# -*- coding: utf-8 -*-
import logging
from odoo.http import request
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED
from .response import error_response, success_message_response
from odoo.modules.registry import Registry
from odoo.tests import get_db_name

# import jsons
_logger = logging.getLogger(__name__)

registry = Registry(get_db_name())


def wrap__resource__delete_one(modelname: str, id: int):
    # Try delete the object
    cr, uid = registry.cursor(), request.session.uid
    cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    Model = request.env(cr, uid)[modelname]
    try:
        Model.browse(id).unlink()
        cr.commit()
        cr.close()
        return success_message_response(status=200, message='Delete Successfully.')
    except Exception as e:
        if not cr.closed:
            cr.close()
        return error_response(status=409, odoo_error=str(e))
