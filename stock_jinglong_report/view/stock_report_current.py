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

from openerp import tools
from openerp.osv import fields, osv

class stock_report_current(osv.osv):
    _name = "stock.report.current"
    _description = "Stock report current"
    _auto = False
    _rec_name = 'product_id'

    _columns = {
        'id': fields.integer('id', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'lot_id': fields.many2one('stock.production.lot', 'Lot', readonly=True),
        'qty': fields.float('qty', readonly=True),
        'location_id': fields.many2one('stock.location', 'Location', readonly=True),
        'in_date': fields.datetime('Date', readonly=True),
        'a': fields.many2one('product.attribute.value', 'a', readonly=True),
        'b': fields.many2one('product.attribute.value', 'b', readonly=True),
        'c': fields.many2one('product.attribute.value', 'c', readonly=True),
        'd': fields.many2one('product.attribute.value', 'd', readonly=True),
    }
    _order = 'in_date desc'

    def init(self, cr):

        """
            CRM Lead Report
            @param cr: the current row, from the database cursor
        """
        tools.drop_view_if_exists(cr, 'stock_report_current')
        cr.execute("""
            CREATE OR REPLACE VIEW stock_report_current AS (
               select q.id,q.product_id,q.lot_id,q.qty,q.location_id,q.in_date,p.a,p.b,p.c,p.d from stock_quant q  LEFT JOIN (SELECT * FROM crosstab('select pv.prod_id,pa.attribute_id,pv.att_id from product_attribute_value_product_product_rel pv  LEFT JOIN product_attribute_value pa on pv.att_id=pa.id order by prod_id,attribute_id
')  AS pav(prod_id integer,a integer,b integer,c integer,d integer)) p on q.product_id=p.prod_id

            )""")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
