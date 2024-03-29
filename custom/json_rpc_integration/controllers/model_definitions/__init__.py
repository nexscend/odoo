from .sale_order import sale_order_fields
from .product_template import product_template_fields

models = {
    'sale.order': sale_order_fields,
    'product.template': product_template_fields,
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
