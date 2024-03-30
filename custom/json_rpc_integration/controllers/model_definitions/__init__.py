from .sale_order import sale_order_fields
from .product_template import product_template_fields
from .product_category import product_category_fields
from .product_attribute import product_attribute_fields
from .res_users import res_users_fields
from .res_partner import res_partner_fields

models = {
    'sale.order': sale_order_fields,
    'product.template': product_template_fields,
    'product.category': product_category_fields,
    'product.attribute': product_attribute_fields,
    'res.users': res_users_fields,
    'res.partner': res_partner_fields,
}

# README : base register model

# base_fields = {
#     'is_public': True,
#     'default_list_domains': [],
#     'list_fields': (
#         'id',
#         'name',
#         'create_date'
#     ),
#     'detail_fields': (
#         'id',
#         'name',
#         'create_date'
#     ),
#     'default_create_fields': {}
# }

# README : add to models dict
