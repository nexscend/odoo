product_category_fields = {
    'default_list_domains': [],
    'list_fields': [
        'id',
        'name',
        ('parent_id', {'id', 'name'}),
        'complete_name',
    ],
    'detail_fields': [
       'id',
        'name',
        ('parent_id', {'id', 'name'}),
        'complete_name',
    ],
    'fields': [
       'id',
        'name',
        ('parent_id', {'id', 'name'}),
        'complete_name',
    ],
    'default_create_fields': {}
}
