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

    def autorizar_solicitante(self):
        for compra in self:
            compra.solicitante = True
        return True

    def autorizar_jefe_director(self):
        for compra in self:
            compra.jefe_director = True
        return True

    def autorizar_director_financiero_local(self):
        for compra in self:
            compra.director_financiero_local = True
        return True

    def autorizar_gerente_general_local(self):
        for compra in self:
            compra.gerente_general_local = True
        return True

    def autorizar_gerente_compras_ca(self):
        for compra in self:
            compra.gerente_compras_ca = True
        return True

    def autorizar_director_proceso_ca(self):
        for compra in self:
            compra.director_proceso_ca = True
        return True

    def autorizar_director_financiero_ca(self):
        for compra in self:
            compra.director_financiero_ca = True
        return True

    def autorizar_director_general_ca(self):
        for compra in self:
            compra.director_general_ca = True
        return True

    def button_confirm(self):
        res = super().button_confirm()
        for order in self:
            if order.currency_id.name == "USD":
                if order.amount_total <= 1499:
                    if order.solicitante and order.jefe_director and order.director_financiero_local and order.gerente_general_local:
                        return res
                    else:
                        raise UserError(_("La orden debe de ser validada por los primeros 4 autorizadores"))
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