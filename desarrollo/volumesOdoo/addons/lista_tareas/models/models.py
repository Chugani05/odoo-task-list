# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ListaTareas(models.Model):
    _name = 'lista_tareas.lista_tareas'
    _description = 'Lista de tareas'

    tarea = fields.Char(string='Tarea')
    prioridad = fields.Integer(string='Prioridad')
    urgente = fields.Boolean(
        string='Urgente',
        compute='_check_urgency',
        store=True
    )
    realizada = fields.Boolean(string='Realizada')
    asignado_a = fields.Many2one('res.users', string='Asignado a', required=False, default=lambda self: self.env.user)
    fecha_limite = fields.Date(string='Fecha limite', required=False)
    fecha_creacion = fields.Datetime(string='Fecha de creacion', default=lambda self: fields.Datetime.today())
    retrasada = fields.Boolean(string='retrasada', compute='_check_delayed', store=True)

    @api.depends('prioridad')
    def _check_urgency(self):
        for record in self:
            record.urgente = record.prioridad > 10

    @api.depends('fecha_limite', 'retrasada')
    def _check_delayed(self):
        for record in self:
            if record.fecha_limite: 
                record.realizada = False and record.fecha_limite < fields.Date.today()
            else:
                record.retrasada = False