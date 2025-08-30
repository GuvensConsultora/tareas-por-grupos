# -*- coding: utf-8 -*-
from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    agrupar = fields.Selection(
        selection=[
            ('1', '1er Grupo'),
            ('2', '2do Grupo'),
            ('3', '3er Grupo'),
            ('4', '4to Grupo'),
        ],
        string='Agrupar',
        required=False,
    )

    fsm_order_ids = fields.One2many(
        comodel_name='fsm.order',
        inverse_name='sale_order_line_id',
        string='Órdenes FSM'
    )
class FSMOrder(models.Model):
    _inherit = 'fsm.order'  # requiere el módulo de Field Service instalado

    sale_order_line_id = fields.Many2one(
        comodel_name='sale.order.line',
        string='Línea de venta',
        ondelete='set null',
        index=True,
        copy=False,
    )

    # (Opcional) atajo al pedido para búsquedas/acciones
    sale_order_id = fields.Many2one(
        related='sale_order_line_id.order_id',
        string='Pedido de venta',
        store=True,
        readonly=True,
        index=True,
    )

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_create_fsm_orders(self):
        """Crea una fsm.order por cada línea elegible que no tenga aún."""
        self.ensure_one()
        Fsm = self.env['fsm.order']
        created = Fsm.browse()

        for line in self.order_line:
            # saltar secciones/notas
            if line.display_type:
                continue
            # (opcional) limitar a productos de tipo servicio
            if line.product_id and line.product_id.type != 'service':
                continue
            # evitar duplicados por línea
            if line.fsm_order_ids:
                continue

            vals = {
                'customer_id': self.partner_id.id,   # cliente
                'company_id': self.company_id.id,
                'sale_order_line_id': line.id,
                'name': f"{self.name or 'SO'} - {line.product_id.display_name or line.name}",
            }
            # si FSM tiene estos campos, seteamos fechas desde la orden
            if 'scheduled_date_start' in Fsm._fields and self.commitment_date:
                vals['scheduled_date_start'] = self.commitment_date
            if 'scheduled_date_end' in Fsm._fields and self.commitment_date:
                vals['scheduled_date_end'] = self.commitment_date

            created |= Fsm.create(vals)

        if created:
            # log en el chatter
            self.message_post(
                body=f"Se crearon {len(created)} órdenes FSM: " +
                ", ".join(created.mapped('name'))
            )
            # abrir las recién creadas
            return {
                'name': 'Órdenes FSM creadas',
                'type': 'ir.actions.act_window',
                'res_model': 'fsm.order',
                'view_mode': 'tree,form,kanban',
                'domain': [('id', 'in', created.ids)],
                'target': 'current',
            }
        # notificación si no se creó nada
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Nada para crear',
                'message': 'No hay líneas elegibles (ya tienen orden, son secciones/notas o no son servicios).',
                'type': 'warning',
                'sticky': False,
            }
        }
