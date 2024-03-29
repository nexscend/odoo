import logging
from .utils import get_fields_values_from_model
from .response import error_response, success_list_response

_logger = logging.getLogger(__name__)


def wrap__resource__read_all(modelname, default_domain, OUT_fields, exclude_fields=None, pre_schema=True,
                             **jdata):
    # Default filter
    domain = default_domain or []
    # Get additional parameters
    if 'filters' in jdata:
        domain += eval(jdata['filters'])
    offset = jdata.get('offset', 0)
    limit = jdata.get('limit', None)
    order = jdata.get('order', None)
    # Dynamically exclude fields (from predefined schema)
    if exclude_fields:
        if type(exclude_fields) == str:
            exclude_fields = (exclude_fields,)
        if {'*', '__all_fields__'}.intersection(set(exclude_fields)):
            OUT_fields = ('id',)
        else:
            new_OUT_fields = ()
            for ff in OUT_fields:
                fk = ff[0] if type(ff) == tuple else ff
                if fk not in exclude_fields:
                    new_OUT_fields += (ff,)
            OUT_fields = new_OUT_fields

    # Reading object's data:
    try:
        Objects_Data = get_fields_values_from_model(
            modelname=modelname,
            domain=domain,
            offset=offset,
            limit=limit,
            order=order,
            fields_list=OUT_fields,
            pre_schema=pre_schema,
        )
    except Exception as e:
        return error_response(status=409, odoo_error=str(e))
    return success_list_response(data=Objects_Data)
