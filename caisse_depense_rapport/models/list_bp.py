
from odoo import models, fields, api
class Liste_bp(models.Model):
    _name='bp.list'
    _description='choix des bp'
    
    name=fields.Char(string='Nom')
    encaisseur_id = fields.Many2one('hr.employee',store=True, string="Encaisseur",related='bp_id.encaisseur_id')
    