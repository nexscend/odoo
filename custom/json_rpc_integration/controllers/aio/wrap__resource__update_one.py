import logging
import json
from ast import literal_eval
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

from odoo.modules.registry import Registry
from odoo.tests import get_db_name
from odoo.http import request

from .utils import convert_values_from_jdata_to_vals, get_fields_values_from_model
from .response import success_message_response, error_response

# import jsons
_logger = logging.getLogger(__name__)

registry = Registry(get_db_name())


def wrap__resource__update_one(modelname: str, id: int, **data):
    vals = convert_values_from_jdata_to_vals(modelname, data, creating=False)
    # Try update the object
    cr, uid = registry.cursor(), request.session.uid
    cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    Model = request.env(cr, uid)[modelname]
    try:
        Model.browse(id).write(vals)
        cr.commit()
        cr.close()
        return success_message_response(200, message='Update Successfully.')
    except Exception as e:
        if not cr.closed:
            cr.close()
        return error_response(status=409, odoo_error=str(e))
