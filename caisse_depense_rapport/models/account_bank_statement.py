from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError,Warning
from datetime import datetime,date

class Caisse_liquidite(models.Model):
    _inherit = 'account.bank.statement'
    _description = "creer un bp"
    
    
    def valider_2(self):
        for line in self.line_ids:
            if line.payment_ids:
                if line.statut != 'valider':
                    line.payment_ids.write({'state': 'controle'})
                    line.payment_ids.write({'state1': 'controle'})
                    line.write({'statut': 'valider'})
                    if line.payment_ids.type_depense=="bp":
                            self.env['caisse_depense_rapport.bpjournalier'].create({
                                        'bp_id':line.payment_ids.id,
                                        'statut':"draft"
                                        }) 
                            rapport=self.env['rapport.acheteur'].search([('bp_id','=',line.payment_ids.id)])
                            if rapport:
                                for bp in rapport:
                                    bp.statut="bigining" 
                    if line.payment_ids.type == "payment_forni":

                        line.payment_ids._create_move_entry() 
                        for payment in line.payment_ids.payment_lines:
                            if payment.invoice_id:
                                payment.invoice_ids = [(6, 0, payment.invoice_id.ids)]
                                payment.action_validate_invoice_payment()
                                payment.invoice_id.write({'en_paiement': False})
                                payment.invoice_id.write({'bash_state': 'controle'})
                                
                        line.payment_ids._create_move_entry_contreparti()
                        line.payment_ids.move.post()


                    elif line.payment_ids.type == "baf":
                        line.payment_ids._create_move_entry()
                        for payment in line.payment_ids.payment_lines:
                           payment.post()
                        line.payment_ids._create_move_entry_contreparti()
                        line.payment_ids.move.post()

                    
                        
                    elif line.payment_ids.type == "pmt":

                        if not line.payment_ids.payment_lines:
                            line.payment_ids.action_lettrage()
                            # line.payment_ids.move.post()
                        else:

                            line.payment_ids._create_move_entry()
                            for payment in line.payment_ids.payment_lines:
                                if payment.invoice_id:
                                    payment.invoice_ids = [(6, 0, payment.invoice_id.ids)]
                                    payment.action_validate_invoice_payment()
                                    payment.invoice_id.write({'en_paiement': False})
                                    payment.invoice_id.write({'bash_state': 'controle'})
                               # payment.post()
                            line.payment_ids._create_move_entry_contreparti()
                            line.payment_ids.move.post()
                            
                    elif line.payment_ids.type == "depense":
                        line.payment_ids._create_move_entry()
                        for payment in line.payment_ids.payment_lines:
                            payment.post()
                            payment.project_id.write({'state': 'paid'})
                            payment.project_id.action_comptabiliser()
                            payment.project_id.write({'en_paiement': False})
                        line.payment_ids._create_move_entry_contreparti()
                        line.payment_ids.move.post()
                        # payment.post()
                    else:
                        line.payment_ids._create_move_entry()
                        for payment in line.payment_ids.payment_lines:
                            payment.post()
                            payment.project_id.write({'state': 'paid'})
                            payment.project_id.write({'en_paiement': False})
                        line.payment_ids._create_move_entry_contreparti_2()
                        line.payment_ids.move.post()
            else:
                if line.appro_id:
                    line.appro_id.comptabilisation(line.journal_id)
                line.write({'statut': 'valider'})
        return True
    
    
    def cancel_caisse_2(self):
        for rec in self:
            rec.write({'state':'open'})

        for record in self.line_ids:
            record.write({'statut':'valider'})
            # if record.payment_ids.type_depense=="bp":
            #         self.env['caisse_depense_rapport.bpjournalier'].search([('bp_id','=',record.payment_ids.id)],[]).unlink()
            #         rapport=self.env['rapport.acheteur'].search([('bp_id','=',record.payment_ids.id)])
            #         for bp in rapport:
            #             bp.statut="draft" 
        
                    
               