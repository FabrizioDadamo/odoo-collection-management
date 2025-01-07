

{
    'name': 'Collection Management',
    'version': '16.0.1.0.0',
    'author': 'Fabrizio D Adamo - ABC-Strategie',
    'website': 'https://www.abcstrategie.it',
    'category': 'Operations/Collection',
    'summary': 'Gestione dei punti di raccolta e movimenti di materiali/rifiuti.',
    'description': """
Modulo stand-alone per Odoo 16 che consente:
- Gestione dei punti di raccolta (capacity, localizzazione, ecc.)
- Movimenti di materiali con stato (In attesa, Smaltito, Consegnato a terzi)
- Reminder di scadenza smaltimento
- Report e statistiche su quantità raccolte nel tempo
    """,
    'depends': [
        'base',
        'mail',
        # 'calendar',
    ],
    'data': [
        'security/security.xml',                
        'security/ir.model.access.csv',         
        'views/collection_point_views.xml',
        'views/material_type_views.xml',
        'views/collection_movement_views.xml',
        'views/menus.xml',
        'data/reminder_cron.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'collection_management/static/src/css/style.css',
        ],
    },
    'installable': True,
    'application': True,
}
