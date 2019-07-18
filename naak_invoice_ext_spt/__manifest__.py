# -*- coding: utf-8 -*-
{
    'name': 'Naak Invoice Ext',
    'category': 'Other',
    'sequence': 1,
    'version': '12.0.0.1',
    'author': 'SnepTech',
    'license': 'AGPL-3',
    'website': 'https://sneptech.com/',

    'summary': 'invoice flow customization',
    'description': """

    """,
    'depends': ['base','sale_management','purchase'],
    'data': [
        'date/cron.xml',
        'views/sale_order_view.xml',
    ],
    

    'installable': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
