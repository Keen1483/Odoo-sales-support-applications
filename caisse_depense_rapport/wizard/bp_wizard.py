from odoo import models, fields,api,exceptions,_
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
import datetime


class Wizardpayment(models.TransientModel):
	
    _name="account.bash.payment.wizard"
    _description="justification par wizard"
    
    def get_default_bp(self):
        return self.env['account.bash.payment'].browse(self.env.context.get('active_ids'))
    
    justication_bp=fields.Text(string="Justification de bp", store=True)
    bp_id=fields.Many2one('account.bash.payment', string="Bon provisoire",default=get_default_bp)
    name = fields.Char(string="nom")
    
    def method_hors_justification(self):
        for elt in self:
                   
            # self.env['rapport.acheteur'].create({
            #         'bp_id':elt.bp_id.id,
            #         'statut':"draft",
            #         'justification':elt.justication_bp,
            #         'justif_value':True
            #          })
            self.env['account.bash.payment'].browse(elt.bp_id.id).action_valide_depense3(elt.justication_bp)
            
            print("id de bp",elt.bp_id.id)
    
    @api.multi
    def call_wizard2(self):
        print ("call wizard fucntion")
        wizard_form = self.env.ref('caisse_depense_rapport.wizard_form_bp', False)
        view_id = self.env['account.bash.payment.wizard']
        vals = {
                    'name'   : 'this is for set name',
                }
        new = view_id.create(vals)
        return {
                    'name'      : _('Hi I am wizard, I am from python code'),
                    'type'      : 'ir.actions.act_window',
                    'res_model' : 'account.bash.payment.wizard',
                    'res_id'    : new.id,
                    'view_id'   : wizard_form.id,
                    'view_type' : 'form',
                    'view_mode' : 'form',
                    'target'    : 'new'
                }

    
   
        
 
 
 
