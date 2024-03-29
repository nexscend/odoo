import logging
import json
from ast import literal_eval
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED

from odoo.modules.registry import Registry
from odoo.tests import get_db_name
from odoo.http import request

from .utils import convert_values_from_jdata_to_vals, get_fields_values_from_model
from .response import success_response, error_response

# import jsons
_logger = logging.getLogger(__name__)

registry = Registry(get_db_name())


def wrap__resource__create_one(modelname, default_vals, OUT_fields=('id',), **data):
    vals = convert_values_from_jdata_to_vals(modelname, data)
    # Set default fields:
    if default_vals:
        vals.update(default_vals)
    # Try create new object
    cr, uid = registry.cursor(), request.session.uid
    cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    Model = request.env(cr, uid)[modelname]
    try:
        new_id = Model.create(vals).id
        cr.commit()
        cr.close()
        # protection against only one item without a comma
        if type(OUT_fields) == str:
            OUT_fields = (OUT_fields,)
        # Handling of archived (non active) Odoo record:
        domain = [('id', '=', new_id)]
        if 'active' in vals:
            domain += [('active', '=', vals.get('active'))]

        response_json = get_fields_values_from_model(
            modelname=modelname,
            domain=domain,
            fields_list=OUT_fields
        )[0]
        return success_response(status=201, **response_json)
    except Exception as e:
        if not cr.closed:
            cr.close()
        return error_response(status=409, odoo_error=str(e))
