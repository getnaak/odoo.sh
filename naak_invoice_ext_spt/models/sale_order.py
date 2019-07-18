from odoo import models, fields, api, _
from datetime import datetime

class sale_order(models.Model):           
    _inherit = 'sale.order'

    schedul_date = fields.Date('Schedul Date', compute='_get_schedul_date',store=True)
    payment_request_done = fields.Boolean('Request Done')
    purchase_ids = fields.One2many('purchase.order','sale_order_id','Purchase Orders')

    @api.multi
    @api.depends('purchase_ids','purchase_ids.picking_ids','purchase_ids.picking_ids.date_done')
    def _get_schedul_date(self):
        purchase_obj = self.env['purchase.order']
        picking_obj = self.env['stock.picking']
        for record in self:
            purchase_ids = purchase_obj.search([('sale_order_id','=',record.id)]).ids
            date_done = [] 
            picking_recs = picking_obj.search([('purchase_id','in',purchase_ids)])
            for pick in picking_recs:
                if pick.state == 'done' and pick.date_done != False:
                    date_done.append(pick.date_done)
            if len(date_done) == len(picking_recs) and len(picking_recs) != 0:
                date = max(date_done)
                record.schedul_date = date.date()

    @api.multi
    def raise_purchase_order(self):
        form_view = self.env.ref('purchase.purchase_order_form')

        return {
            'name': _('Purchase Order'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'views': [(form_view.id, 'form')],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context':{
                'default_sale_order_id' : self.id,
            },
        }
    
    @api.multi
    def cron_payment_request(self):
        purchase_obj = self.env['purchase.order']
        advance_payment_obj = self.env['sale.advance.payment.inv']
        down_product = self.env['ir.config_parameter'].search([('key','=','sale.default_deposit_product_id')])
        template = self.env.ref('account.email_template_edi_invoice')
        orders = self.search([('schedul_date','<=',datetime.now().date()),('payment_request_done','=',False),('state','!=','cancel')])
        for order in orders:
            order_line_product = []
            for line in order.order_line:
                order_line_product.append(line.product_id.id)
            if int(down_product.value) in order_line_product:
            
                advance_payment_obj = advance_payment_obj.with_context(active_ids=order.ids)
                
                advance_payment_rec = advance_payment_obj.create({'advance_payment_method':'all'})
                advance_payment_rec.create_invoices()
                order.invoice_ids[0].action_invoice_open()
                template.send_mail(order.invoice_ids[0].id,force_send=True)
                order.payment_request_done = True