res_users_fields = {
    'default_list_domains': [],
    'list_fields': [
         'id',
        'active',
        'login',
        ('company_id', {'id', 'name'}),
        ('partner_id', {'id', 'name'}),
        ('sale_team_id', {'id', 'name'}),
        ('website_id', {'id', 'name'}), 
    ],
    'detail_fields': [
         'id',
        'active',
        'login',
        ('company_id', {'id', 'name'}),
        ('partner_id', {'id', 'name'}),
        ('sale_team_id', {'id', 'name'}),
        ('website_id', {'id', 'name'}),
    ],
    'fields': [
         'id',
        'active',
        'login',
        ('company_id', {'id', 'name'}),
        ('partner_id', {'id', 'name'}),
        ('sale_team_id', {'id', 'name'}),
        ('website_id', {'id', 'name'}),
    ],
    'default_create_fields': {}
}
