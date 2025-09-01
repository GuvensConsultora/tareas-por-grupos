# -*- coding: utf-8 -*-
from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)


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

    task_id = fields.Many2one(
        "project.task",
        string="Tarea relacionada",
        domain=[],

        help="Vinculá una tarea a esta línea de venta."
     )


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_generate_group_tasks(self):

        """Genera/asigna una tarea por cada grupo (x_project_id) en las líneas sin tarea."""
        Task = self.env["project.task"]
        for order in self:
            # cache local para no buscar/crear repetido en la misma ejecución
            cache_task_by_group = {}

            # Tomamos solo líneas “reales”
            solines = order.order_line.filtered(lambda l: not l.display_type)
            _logger.info("[TASKGEN] Líneas reales a procesar: %s", [l.id for l in solines])

            for line in solines:
                _logger.info("LINEA: %s, GRUPO: %s, TAREA: %s", line.id, line.agrupar, line.task_id)
                # Si ya tiene tarea o no tiene grupo → saltar
                if line.task_id or not line.agrupar:
                    continue

                group = line.agrupar
                task = cache_task_by_group.get(group)

                if not task:
                    # Intentar reutilizar una tarea existente de este pedido y grupo
                    # Estrategia: buscar por (project_id == grupo) y nombre que empiece con el nombre del pedido.
                    # Podés refinar el dominio si preferís otro identificador.
                    name_prefix = f"{order.name} - {order.partner_id.name} - {line.agrupar}"
                    task = Task.search([
                        ("project_id", "=", group),
                        ("name", "=", name_prefix),
                    ], limit=1)

                    if not task:
                        # Crear la tarea
                        vals = {
                            "name": name_prefix,
                            "proyect_id": 2,
                            "partner_id": order.partner_id.id,
                            "sale_order_id":order.id,
                            "description": f"Tarea generada desde {order._name} {order.name}",
                            # opcional: asignar responsable
                            # "user_id": order.user_id.id,
                        }
                        task = Task.create(vals)

                    cache_task_by_group[group] = task

                # Asignar la tarea encontrada/creada a la línea
                line.task_id = task.id

        return True
