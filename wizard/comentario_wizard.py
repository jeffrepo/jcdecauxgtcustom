# -*- coding: utf-8 -*-
from odoo import fields, models, _
import logging
from odoo.exceptions import UserError, ValidationError

class ComentarioWizard(models.TransientModel):
        _name = "comentario.wizard"
        _description = 'Comentario wizard'
        
        message = fields.Text(string="Mensaje")
       
        def confirmar(self):
            usuario = self.env.context.get('usuario')
            orden_id = self.env.context.get('active_id')
            orden = False
            orden = self.env["purchase.order"].search([('id','=', orden_id)])
            if orden:
                mensaje = 'Usuario: '+ usuario + ' No autorizó, razón: ' + self.message
                orden.message_post(body= mensaje, subject="No autorizado", email_from=False)
                orden.no_autorizado = True
            return {'type': 'ir.actions.act_window_close'}