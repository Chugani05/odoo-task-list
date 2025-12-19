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
    realizada = fields.Boolean(string='Realizada', compute='_check_done', store=True)
    asignado_a = fields.Many2one('res.users', string='Asignado a', required=False, default=lambda self: self.env.user)
    fecha_limite = fields.Date(string='Fecha limite', required=False)
    fecha_creacion = fields.Datetime(string='Fecha de creacion', default=lambda self: fields.Datetime.now())
    retrasada = fields.Boolean(string='Retrasada', compute='_check_delayed', store=True)
    estado = fields.Selection([
                                ('nuevo', 'Nueva'), 
                                ('progreso', 'En curso'), 
                                ('bloqueado', 'Bloqueada'), 
                                ('hecho', 'Hecha')
                            ], 
                              string="Estado", 
                              default="nuevo", 
                              compute='_check_state', 
                              store=True
                            )

    @api.depends('prioridad')
    def _check_urgency(self):
        for record in self:
            record.urgente = record.prioridad > 10

    @api.depends('fecha_limite', 'retrasada')
    def _check_delayed(self):
        for record in self:
            if record.fecha_limite: 
                record.retrasada = not record.realizada and record.fecha_limite < fields.Date.today()
            else:
                record.retrasada = False

    @api.depends('realizada')
    def _check_state(self):
        for record in self:
            if record.realizada:
                record.estado = "hecho"

    @api.depends('estado')
    def _check_done(self):
        for record in self:
            record.realizada = record.estado == "hecho"

    def set_state_to_in_progress(self):
        self.write({'state': "progreso"})

    def set_state_to_blocked(self):
        self.write({'state': "bloqueado"})

    def set_state_to_done(self):
        self.write({'state': "hecho"})
