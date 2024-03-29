sale_order_fields = {
    'default_list_domains': [],
    'list_fields': [
        'id',
        ('partner_id', {'id', 'name'}),
        'date_order',
        ('order_line', [(
            "id",
            "name",
            ("product_template_id", {
                "id",
                "name",
            }),
            "product_uom_qty",
            "price_unit",
            "price_subtotal",
            ("currency_id", {
                "id",
                "name"
            }),
        )])
    ],
    'detail_fields': [
        'id',
        ('partner_id', {'id', 'name','image_1920'}),
        'date_order',
        ('order_line', [(
            "id",
            "name",
            ("product_template_id", {
                "id",
                "name",
            }),
            "product_uom_qty",
            "price_unit",
            "price_subtotal",
            ("currency_id", {
                "id",
                "name"
            }),
        )])
    ],
    'default_create_fields': {}
}
