{
    'name': 'نظام الأرشيف المتكامل',
    'version': '17.0.1.0.0',
    'summary': 'نظام إدارة الأرشيف الوثائقي',
    'description': '''
    نظام متكامل لإدارة الأرشيف الورقي والإلكتروني
    مع دعم التصنيف الهرمي والتتبع الكامل
    ''',
    'category': 'Productivity/Documents',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': ['base', 'documents','mail'],
    'data': [
        'security/archive_security.xml',
        'security/ir.model.access.csv',
        'data/archive_data.xml',
        'views/archive_views.xml',
        'views/document_views.xml',
        'views/archive_menus.xml',
        # 'views/archive_all_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'docflex_archive/static/src/scss/archive.scss',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}