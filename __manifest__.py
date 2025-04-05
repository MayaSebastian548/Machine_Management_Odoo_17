{
    'name': "Machine Management",
    'version': '17.0.1.0.0',
    'depends': ['web', 'contacts', 'product','mail', 'website'],
    'author': "Chris Ben",
    'category': 'Machine',
    'description': """
    Machine Management
    """,
    'data': [
        'security/machine_management_groups.xml',
        'security/ir.model.access.csv',
        'security/machine_management_security.xml',
        'report/ir_actions_report.xml',
        'report/machine_transfer_report_template.xml',
        'data/website_menu_data.xml',
        'data/service_product_data.xml',
        'data/email_template_data.xml',
        'data/ir_cron.xml',
        'data/transfer_sequence_data.xml',
        'data/machine_type_data.xml',
        'data/machine_tags_data.xml',
        'wizard/machine_transfer_wizard_views.xml',
        'views/snippets/s_machine_template.xml',
        'views/website_machine_form_views.xml',
        'views/website_service_list_views.xml',
        'views/website_service_form_views.xml',
        'views/machine_transfer_views.xml',
        'views/machine_manage_views.xml',
        'views/machine_type_views.xml',
        'views/machine_tags_views.xml',
        'views/customer_machines_views.xml',
        'views/machine_service_views.xml',
        'views/machine_info_views.xml',
        'views/machine_menus.xml',
    ],
    'application': True,
    'installable': True,
    'assets': {
        'web.assets_backend': [
            'machine_management/static/src/js/action_manager.js',
        ],
        'web.assets_frontend': [
            'machine_management/static/src/xml/s_machine.xml',
            'machine_management/static/src/js/machine_snippet.js',
        ],
    }
}
