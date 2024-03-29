from .utils import get_fields_values_from_model
from .response import error_response,success_response
def wrap__resource__read_one(modelname, id: int, OUT_fields, pre_schema=True, exclude_fields=None,):
    print("____wrap__resource__read_one___-")
    print("___OUT_fields____-",OUT_fields)
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
        Object_Data = get_fields_values_from_model(
            modelname=modelname,
            domain=[('id', '=', id)],
            fields_list=OUT_fields,
            pre_schema=pre_schema,
        )
    except Exception as e:
        return error_response(status=409, odoo_error=str(e))
    if Object_Data:
        return success_response(status=200, data=Object_Data[0])
    else:
        return error_response(status=404, odoo_error="Object Not Found.")
