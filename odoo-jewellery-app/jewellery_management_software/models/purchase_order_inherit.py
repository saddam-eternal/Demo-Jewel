# -*- coding: utf-8 -*-
# Developed by Eternal Web Pvt Ltd.

import requests
from odoo import fields, models, api, tools, SUPERUSER_ID, http
from odoo.http import request
from odoo.tools.float_utils import float_compare, float_round

class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    def gross_weight_btn(self):
        purchase_order_lines = self.env['purchase.order.line'].search([], order='order_id, id')
        ref_no_set = set()
        ref_no_list = []

        for line in purchase_order_lines:
            if line.order_id.id == self._origin.id:
                ref_no_id = line.ref_no.id
                if ref_no_id not in ref_no_set and ref_no_id:
                    ref_no_set.add(ref_no_id)
                    ref_no_list.append(ref_no_id)
                    # print(f"Product ID: {ref_no_id}, Product Name: {line.ref_no.name}")

        for ref_no_id in ref_no_list:
            gross_weight_total_in_gram = 0

            for line in purchase_order_lines:
                    if line.order_id.id == self._origin.id and ref_no_id == line.ref_no.id:

                        if line.uom_two.name == 'g':
                            # print(f"Order ID: {line.order_id.id}, Line ID: {line.id}, Product Name: {line.product_id.name}")
                            gross_weight_total_in_gram += line.product_qty_two

                        # else:
                        #     gross_weight_total_in_gram = 0
                        #     print(" 1 ============================= gross_weight_total_in_gram: ", gross_weight_total_in_gram)
                        # print(" 2 ============================= gross_weight_total_in_gram: ", gross_weight_total_in_gram)
                        
            for line in purchase_order_lines:
                if line.order_id.id == self._origin.id and ref_no_id == line.ref_no.id and line.product_id.main_product == True:
                    line.write({'gross_weight': gross_weight_total_in_gram - 1,})  


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    @tools.ormcache()
    def _get_default_uom_id_2(self):
        return self.env.ref('uom.product_uom_unit')
    
    uom_two = fields.Many2one('uom.uom', 'UoM 2',default=_get_default_uom_id_2, required=True,help="Default unit of measure used for all stock operations.")
    product_qty_two = fields.Float(string='Quantity 2', default=0, digits='Product Unit of Measure', required=True, compute='_compute_product_qty', store=True, readonly=False)
    ref_no = fields.Many2one('product.product', "Ref No")
    purity_ratio = fields.Float(string="Purity", default=0.0, required=True)
    gross_weight = fields.Float(string="Gross Weight",  default=0.0, required=True)
    piece = fields.Integer(string="Piece", default=0, required=True)

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            if self.product_id.main_product == True:
                purity_ratio = self.product_id.uom_id_2.factor
            else:
                purity_ratio = 0

            self.write({
                'uom_two': self.product_id.uom_id_2,
                'purity_ratio': purity_ratio / 10,
            })

        if self.product_id:
            for line in self.order_id.order_line:
                if line.product_id.main_product == True:
                    line.write({'ref_no': line.product_id.id,})
                else:
                    for l in self.order_id.order_line:  
                        if l.product_id.main_product == True:
                            line.write({'ref_no': l.product_id.id,})

    @api.onchange('product_qty')
    def _onchange_product_qty(self):
        if self.product_id:
            for line in self.order_id.order_line:
                product_qty = self.product_qty
                uom_ratio = self.product_uom.ratio
                uom_two_ratio = self.uom_two.ratio

                if uom_ratio != 0:
                    qty_two_val = (product_qty * uom_two_ratio) / uom_ratio
                else:
                    qty_two_val = 0

                line.write({                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                    'product_qty_two': qty_two_val,
                })
