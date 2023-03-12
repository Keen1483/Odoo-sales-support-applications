# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GestionDocumentsBTI(models.Model):
    _name = 'gestion.documents.bti'
    _inherit = ['mail.thread']
    _description = "gestion sequentiel des document BTI"

    name = fields.Char(string='Nom')
    description = fields.Text(string='Description')
    res_user = fields.Many2one(string='Responsable')
    start_number = fields.Integer(string='Nombre de Début', copy=False, required=True)
    end_number = fields.Integer(string='Nombre de Fin', copy=False, required=True)
    opening_date = fields.Date(string='Date Emission', default=fields.Date.context_today)
    closing_date = fields.Date(string='Date de Cloture')
    type_document = fields.Selection([('bti_vente', 'BTI Vente'), ('bti_achat', 'BTI Achat')], string='Type de document', copy=False, default='bti_vente')
    line_ids = fields.One2many('gestion.documents.bti.line', 'document_id', string='Les Pages', copy=False)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('valid', 'Valider'),
        ('done', 'Terminer'),
        ('cancel', 'Annuler')
    ], string='Status', default='draft', copy=False, index=True, readonly=True, track_visibility='onchange')


class GestionDocumentBTILine(models.Model):
    _name = 'gestion.documents.bti.line'
    _description = 'Les pages du document BTI'

    document_id = fields.Many2one('gestion.documents.bti', string='document')
    #, readonly=True
