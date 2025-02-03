# -*- coding: utf-8 -*-
# Developed by Eternal Web Pvt Ltd.

{
    'name': 'Jewellery Management Software',
    'version': '17.0.0.0',
    'summary': 'Eternal APP Jewellery Management Software',
    'description': """ Eternal APP Jewellery Management Software""",
    'category': 'App',
    'author': 'Eternal Web Pvt Ltd.',
    'maintainer': 'Eternal Web Pvt Ltd.',
    'website':'https://www.eternalsoftsolutions.com',
    'license':'LGPL-3',

    'depends': [
        'base',
        'product',
        'sale_management',
        'purchase',
        'stock'
    ],
    'data': [
        'views/product_template_inherit_view.xml',
        'views/sale_order_inherit_views.xml',
        'views/purchase_order_inherit_views.xml',
    ],

    'images': [
       'static/description/banner.jpg'
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 499.99,
    'currency': 'EUR'
}
