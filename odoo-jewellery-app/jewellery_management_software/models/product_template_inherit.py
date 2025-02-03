# -*- coding: utf-8 -*-
# Developed by Eternal Web Pvt Ltd.

from odoo import fields, models, api, tools, SUPERUSER_ID, http
from odoo.http import request
from odoo.tools.float_utils import float_compare, float_round

class ProductTempleteInherit(models.Model):
    _inherit = 'product.template'

    @tools.ormcache()
    def _get_default_uom_id_2(self):
        return self.env.ref('uom.product_uom_unit')
    main_product = fields.Boolean('Product As Main Product', default=False)
    uom_id_2 = fields.Many2one('uom.uom', 'Unit of Measure 2',default=_get_default_uom_id_2, required=True,help="Default unit of measure used for all stock operations.")