from odoo import http, models, fields
from odoo.http import request
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED
from datetime import date, datetime


def get_fields_values_from_model(modelname, domain, fields_list, offset=0, limit=None, order=None, pre_schema=True):
    cr, uid = request.cr, request.session.uid
    cr._cnx.set_isolation_level(ISOLATION_LEVEL_READ_COMMITTED)
    Model = request.env(cr, uid)[modelname]

    records = Model.search(domain, offset=offset, limit=limit, order=order)
    if not records:
        return {}
    result = []
    for record in records:
        result += [get_fields_values_from_one_record(record, fields_list, pre_schema=pre_schema)]

    return result


def get_fields_values_from_one_record(record, fields_list, pre_schema=True):
    result = {}
    for field in fields_list:
        if type(field) == str:
            val = record[field]
            if pre_schema:
                # If many2one _plane_ field
                try:
                    val = val.id
                except:
                    pass

            # Convert Date/Datetime values to (old) string representation
            if isinstance(val, date):
                if isinstance(val, datetime):
                    val = fields.Datetime.to_string(val)
                else:
                    val = fields.Date.to_string(val)
            # if isinstance(val, bytes) and record._fields[field].type == 'binary':
            #     val = f"/web/image/?model={record._name}&field={field}&id={record.id}"
            if not isinstance(val, models.BaseModel):
                result[field] = val if (val or '0' in str(val)) else None
            # for flat response:
            else:
                result[field] = record[field].ids or None
            if not pre_schema and isinstance(record[field], models.BaseModel) and record[field]:
                if record._fields[field].type == 'many2one':
                    result[field] = {'id': record[field].id}
                    try:
                        result[field]['name'] = record[field].name
                    except:
                        pass
        else:
            # Sample for One2many field: ('bank_ids', [('id', 'acc_number', 'bank_bic')])
            f_name, f_list = field[0], field[1]

            if type(f_list) == list:
                # Many (list of) records
                f_list = f_list[0]
                result[f_name] = []
                recs = record[f_name]
                for rec in recs:
                    result[f_name] += [get_fields_values_from_one_record(rec, f_list)]
            else:
                # One record
                rec = record[f_name]
                # protection against only one item without a comma
                if type(f_list) == str:
                    f_list = (f_list,)
                result[f_name] = get_fields_values_from_one_record(rec, f_list)

    return result


def convert_values_from_jdata_to_vals(modelname, jdata, creating=True):
    cr, uid = request.cr, request.session.uid
    Model = request.env(cr, uid)[modelname]

    x2m_fields = [f for f in jdata if type(jdata[f]) == list]
    f_props = Model.fields_get(x2m_fields)

    vals = {}
    for field in jdata:
        val = jdata[field]
        if type(val) != list:
            vals[field] = val
        else:
            # x2many
            #
            # Sample for One2many field:
            # 'bank_ids': [{'acc_number': '12345', 'bank_bic': '6789'}, {'acc_number': '54321', 'bank_bic': '9876'}]
            vals[field] = []
            field_type = f_props[field]['type']
            # if updating of 'many2many'
            if (not creating) and (field_type == 'many2many'):
                # unlink all previous 'ids'
                vals[field].append((5,))

            for jrec in val:
                rec = {}
                for f in jrec:
                    rec[f] = jrec[f]

                if field_type == 'one2many':
                    if creating:
                        vals[field].append((0, 0, rec))
                    else:
                        if 'id' in rec:
                            id = rec['id']
                            del rec['id']
                            if len(rec):
                                # update record
                                vals[field].append((1, id, rec))
                            else:
                                # remove record
                                vals[field].append((2, id))
                        else:
                            # create record
                            vals[field].append((0, 0, rec))

                elif field_type == 'many2many':
                    # link current existing 'id'
                    vals[field].append((4, rec['id']))
    return vals
