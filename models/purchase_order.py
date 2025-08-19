# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
import logging


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    solicitante = fields.Boolean("Solicitante")
    jefe_director = fields.Boolean("Jefe director")
    director_financiero_local = fields.Boolean("Director financiero local")
    gerente_general_local = fields.Boolean("Gerente general local")
    gerente_compras_ca = fields.Boolean("Gerente de compras CA")
    director_proceso_ca = fields.Boolean("Director dl proceso CA")
    director_financiero_ca = fields.Boolean("Director financiero CA")
    director_general_ca = fields.Boolean("Director general CA")
    no_autorizado = fields.Boolean("No autorizado")

    def no_autorizar(self,):
        for compra in self:
            compra.no_autorizado = True
            mensaje = "Solicitud no aprobada por: " + self.env.user.name
            self.message_post(body= mensaje, subject="Solicitud no aprobada", email_from=False)
        return True

    def autorizar_solicitante(self):
        for compra in self:
            compra.solicitante = True
            group_director = self.env.ref('jcdecauxgtcustom.jc_jefe_director')
            users_in_group = group_director.users
            if users_in_group:
                mensaje = "Solicitud aprobacion"
                self.message_post(partner_ids=users_in_group.mapped('partner_id').ids,body= mensaje, subject="Solicitud aprobacion", email_from=False)
        return True

    def autorizar_jefe_director(self):
        for compra in self:
            compra.jefe_director = True
            group_director_financiero_local = self.env.ref('jcdecauxgtcustom.jc_directo_financiero_local')
            users_in_group = group_director_financiero_local.users
            if users_in_group:
                mensaje = "Solicitud aprobacion"
                self.message_post(partner_ids=users_in_group.mapped('partner_id').ids,body= mensaje, subject="Solicitud aprobacion", email_from=False)
        return True

    def autorizar_director_financiero_local(self):
        for compra in self:
            compra.director_financiero_local = True
            group_gerente_general_local = self.env.ref('jcdecauxgtcustom.jc_gerente_general_local')
            users_in_group = group_gerente_general_local.users
            if users_in_group:
                mensaje = "Solicitud aprobacion"
                self.message_post(partner_ids=users_in_group.mapped('partner_id').ids,body= mensaje, subject="Solicitud aprobacion", email_from=False)
        return True

    def autorizar_gerente_general_local(self):
        for compra in self:
            compra.gerente_general_local = True
            if compra.amount_total >= 1500 and compra.amount_total <= 2999:
                group_gerente_compras_ca = self.env.ref('jcdecauxgtcustom.jc_gerente_compras_ca')
                users_in_group = group_gerente_compras_ca.users
                if users_in_group:
                    mensaje = "Solicitud aprobacion"
                    self.message_post(partner_ids=users_in_group.mapped('partner_id').ids,body= mensaje, subject="Solicitud aprobacion", email_from=False)
        return True

    def autorizar_gerente_compras_ca(self):
        for compra in self:
            compra.gerente_compras_ca = True
            if compra.amount_total >= 3000 and compra.amount_total <= 9999:
                group_director_proceso_ca = self.env.ref('jcdecauxgtcustom.jc_director_proceso_ca')
                users_in_group = group_director_proceso_ca.users
                if users_in_group:
                    mensaje = "Solicitud aprobacion"
                    self.message_post(partner_ids=users_in_group.mapped('partner_id').ids,body= mensaje, subject="Solicitud aprobacion", email_from=False)
        return True

    def autorizar_director_proceso_ca(self):
        for compra in self:
            compra.director_proceso_ca = True
            if compra.amount_total >= 3000 and compra.amount_total <= 9999:
                group_director_financiero_ca = self.env.ref('jcdecauxgtcustom.jc_director_financiero_ca')
                users_in_group = group_director_financiero_ca.users
                if users_in_group:
                    mensaje = "Solicitud aprobacion"
                    self.message_post(partner_ids=users_in_group.mapped('partner_id').ids,body= mensaje, subject="Solicitud aprobacion", email_from=False)
        return True

    def autorizar_director_financiero_ca(self):
        for compra in self:
            compra.director_financiero_ca = True
            if compra.amount_total >= 10000:
                group_director_general_ca = self.env.ref('jcdecauxgtcustom.jc_director_general_ca')
                users_in_group = group_director_general_ca.users
                if users_in_group:
                    mensaje = "Solicitud aprobacion"
                    self.message_post(partner_ids=users_in_group.mapped('partner_id').ids,body= mensaje, subject="Solicitud aprobacion", email_from=False)
        return True

    def autorizar_director_general_ca(self):
        for compra in self:
            compra.director_general_ca = True
        return True

    def button_confirm(self):
        res = super().button_confirm()
        for order in self:
            group_solicitante = self.env.ref('jcdecauxgtcustom.jc_solicitante')
            
            if order.currency_id.name == "USD":
                if order.amount_total <= 1499:
                    if order.solicitante and order.jefe_director and order.director_financiero_local and order.gerente_general_local:
                        return res
                    else:
                        raise UserError(_("La orden debe de ser validada por los primeros 4 autorizadores"))

                        #raise UserError(_("La orden debe de ser validada por los primeros 4 autorizadores"))
                if order.amount_total >= 1500 and order.amount_total <= 2999:
                    if order.solicitante and order.jefe_director and order.director_financiero_local and order.gerente_general_local and order.gerente_compras_ca:
                        return res
                    else:
                        raise UserError(_("La orden debe de ser validada por los primeros 5 autorizadores"))
                if order.amount_total >= 3000 and order.amount_total <= 9999:
                    if order.solicitante and order.jefe_director and order.director_financiero_local and order.gerente_general_local and order.gerente_compras_ca and order.director_proceso_ca and order.director_financiero_ca:
                        return res
                    else:
                        raise UserError(_("La orden debe de ser validada por los primeros 7 autorizadores"))
                if order.amount_total >= 10000:
                    if order.solicitante and order.jefe_director and order.director_financiero_local and order.gerente_general_local and order.gerente_compras_ca and order.director_proceso_ca and order.director_financiero_ca and order.director_general_ca:
                        return res
                    else:
                        raise UserError(_("La orden debe de ser validada por los primeros 7 autorizadores"))