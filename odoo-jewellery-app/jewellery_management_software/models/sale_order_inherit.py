# -*- coding: utf-8 -*-
# Developed by Eternal Web Pvt Ltd.

from odoo import fields, models, api, tools, SUPERUSER_ID, http

class SaleOrderField(models.Model):
    _inherit = 'sale.order'

    product_name = fields.Many2one('product.product',"Product Name")
    available_product_ids = fields.Many2many(
        'product.product', string='Available Products', compute='_compute_available_products', store=False)

    @api.depends('order_line')
    def _compute_available_products(self):
        for record in self:
            all_product_ids = record.env['product.product'].search([]).ids
            ordered_product_ids = record.order_line.mapped('product_id.id')
            available_product_ids = [pid for pid in all_product_ids if pid not in ordered_product_ids]
            record.available_product_ids = [(6, 0, available_product_ids)]

    @api.onchange('product_name')
    def _onchange_product_id(self):
        if self.product_name:
            purchase_order_lines = self.env['purchase.order.line'].search([('ref_no.name', '=', self.product_name.name),])

            sale_order_lines = []
            for line in purchase_order_lines:
                sale_order_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_qty,
                    'price_unit': line.price_unit,
                    'uom_two': line.uom_two,
                    'product_qty_two': line.product_qty_two,
                    'ref_no': line.ref_no,
                    'purity_ratio': line.purity_ratio,
                    'gross_weight': line.gross_weight,
                    'piece': line.piece,
                }))
            self.order_line = sale_order_lines


    @tools.ormcache()
    def _get_default_uom_id_2(self):
        return self.env.ref('uom.product_uom_unit')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @tools.ormcache()
    def _get_default_uom_id_2(self):
        return self.env.ref('uom.product_uom_unit')
    
    uom_two = fields.Many2one('uom.uom', 'UoM 2',default=_get_default_uom_id_2, required=True,help="Default unit of measure used for all stock operations.")
    product_qty_two = fields.Float(string='Quantity 2', default=0, digits='Product Unit of Measure', required=True, store=True, readonly=False)
    ref_no = fields.Many2one('product.product', "Ref No")
    purity_ratio = fields.Float(string="Purity", default=0.0, required=True)
    gross_weight = fields.Float(string="Gross Weight",  default=0.0, required=True)
    piece = fields.Integer(string="Piece", default=0, required=True)
    
