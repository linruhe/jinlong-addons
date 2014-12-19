# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _

class stock_production_lot(osv.osv):
    _inherit = 'stock.production.lot'
    _columns = {
        'customer': fields.many2one('res.partner', 'customer',domain=[('customer', '=', 1)]),#客户
        'team': fields.char('team',  help=""),#班组
        'meter': fields.char('meter',  help=""),#卷长
        'num': fields.char('num', help=""),#平米数
        'conumber':fields.char('conumber',help=""),#色号
        'width':fields.float('width',help=""),#宽幅
    }
   
class stock_quant(osv.osv):
    _inherit= 'stock.quant'
    def width_function(self, cr, uid, ids, name, args, context=None):
        res = {}
        for m in self.browse(cr, uid, ids, context=context):
            res[m.id] = m.lot_id.width
        return res
    
    def conumber_function(self, cr, uid, ids, name, args, context=None):
        res = {}
        for m in self.browse(cr, uid, ids, context=context):
            res[m.id] = m.lot_id.conumber
        return res
            
    _columns = {
        'width': fields.function(width_function, type = 'char',string = "width",store=True,readonly=True),         
        'conumber': fields.function(conumber_function, type = 'char',string = "conumber",store=True,readonly=True),
        'meter': fields.related('lot_id', 'meter', type='char', string='meter', help="meter"),
	}
    
    _sql_constraints = [
        #('lot_location_uniq', 'unique (lot_id, location_id)', ''),
    ]


class product_product(osv.osv):
    _inherit = 'product.product'
    
    def test_function(self, cr, uid, ids, name, args, context=None):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            variant = ", ".join([v.name for v in product.attribute_value_ids])
            c_name = variant and "%s (%s)" % (product.name, variant) or product.name
            res[product.id] = c_name
        return res
    
    _columns = {
        'tempname': fields.function(test_function, type = 'char',string = "tempname",store=True,readonly=True),#金额
    }
    
class stock_move(osv.osv):
    _inherit = 'stock.move'
    
    def test_function(self, cr, uid, ids, name, args, context=None):
        res = {}
        for m in self.browse(cr, uid, ids, context=context):
            res[m.id] = m.product_uom_qty * m.money
        return res
 
    def sum_function(self, cr, uid, ids,product_uom_qty,money):
     	result = {
            'Amount': 0.00
        }
        result['Amount'] = product_uom_qty * money
        return {'value': result}
           
    _columns = {
        'number':fields.float('number',required=False, help=""),#卷数
        'money': fields.float('money', required=False, help=""),#价格
        'width': fields.float('width',required=False,  help=""),#宽幅
        'Amount': fields.function(test_function, type = 'float',string = "amount",store=True,readonly=True),#金额
        'conumber':fields.char('conumber',help=""),#色号
    }


class stock_picking(osv.osv):
    _inherit = "stock.picking"
        
    def compute_amount(self,cr,uid,ids,name,args,context=None):
        res = {}
        for i in self.browse(cr,uid,ids,context =context):
            x = 0
        for line in i.move_lines :
            x = x + line.Amount                            
        res[i.id] = x            
        return res
    
    def compute_number(self,cr,uid,ids,name,args,context=None):
        res = {}
        for i in self.browse(cr,uid,ids,context =context):
            x = 0
            for line in i.move_lines :
                x = x + line.number                            
            res[i.id] = x            
        return res
    def compute_squre(self,cr,uid,ids,name,args,context=None):
        res = {}
        for i in self.browse(cr,uid,ids,context =context):
            x = 0
            for line in i.move_lines :
                x = x + line.product_qty                            
            res[i.id] = x            
        return res    
    _columns = {
        'number': fields.function(compute_number,type='float',string ="number",store=True,readonly =True),#卷数
        'Amount': fields.function(compute_amount,type='float',string ="Amount",store=True,readonly =True),#卷数
        'squre': fields.function(compute_squre,type='float',string ="squre",store=True,readonly =True),#平米总数
    }    