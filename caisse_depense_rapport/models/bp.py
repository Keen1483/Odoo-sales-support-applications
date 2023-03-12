from time import strftime
from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError,Warning
from datetime import datetime,date,timedelta

class Bp_op_bpf(models.Model):
    _inherit ="account.bash.payment"
    _description = "liste bp"
    
    
    def action_valide_depense2(self):
        invoice = self.env['caisse_depense.project']
        m_payment = self.env['hr.project_ouvert_lines']
        payment_line = self.env['account.payment']
        inv = []
        dc = 0
        amount = 0
        truth = [val.selection for val in self.project_ouvert_ids if val.amount != 0.0]
        if True in truth:
            dc = dc +1
        if dc >= 1:
        # if self.amount != 0.0:
            # end = m_payment.search([('selection','=',True),('project_id.en_paiement','=',False)])
            end = self.project_ouvert_ids
            for invoice in end:
                if invoice.selection == True and invoice.project_id.en_paiement == False:
                    amount += invoice.amount
                    invoice.project_id.write({'en_paiement': True})
                    invoice.project_id.write({'bash_project_id':self.id})
                    invoice.write({'selection': False})
                    inv = self.account_payment_line2(invoice.project_id)
                    payement = payment_line.create(inv)

            self.write({'en_paiement': 'valide'})
            if self.type_depense != 'bp':
                self.write({'state': 'valide'})
                self.write({'state': 'caisse'})
            else:
                
                employer=self.liste_employer()
                id_encaisseur=self.encaisseur_id.id
                if self.type_depense == 'bp' and id_encaisseur in employer:
                   
                    permision=self.check_permission(id_encaisseur)
                   
                    print('permision', permision)
                    if permision==1:
                        self.write({'state': 'valide'})
                        self.env['rapport.acheteur'].create({
                            'bp_id':self.id,
                            'statut':"draft"
                            })
                    else:
                        message='Monsieur' +' '+ str(self.encaisseur_id.name) +' '+ 'ne peut plus prendre un BP, veuillez rencontrer un responsable'
                        raise Warning(message)
                elif self.type_depense == 'bp' and id_encaisseur not in employer: 
                    print("entre dans la fonction de test des employés")
                    permision=self.check_date(id_encaisseur,2)
                    print("la paermision est", permision)
                    if permision <= 0:
                        self.write({'state': 'valide'})
                    else:
                        print("entre dans la fonction de test des employés choix 2")
                        message='Monsieur'+' '+ str(self.encaisseur_id.name) +' '+ 'ne peut plus prendre un BP, veuillez rencontrer un responsable'
                        raise Warning(message)
                
                     
                     
            self.write({'amount': amount})
            rec = self
            if not rec.name:
                if self.type_depense:
                    comp = self.env.user.company_id.id
                    sequence_code = ''
                    second_code = ''
                    # sequence_code = "hr.bash.depense.%s" % self.type_depense.lower()
                    if self.type_depense == "bp":
                        sequence_code = "hr.bash.depense.bp"
                        second_code = "hr.bash.depense.register"
                        rec.register_seq = self.env['ir.sequence'].search([('company_id','=',comp)]).next_by_code(second_code)
                    elif self.type_depense == "op":
                        sequence_code = "hr.bash.depense.op"
                    else:
                        sequence_code = "hr.bash.depense.%s" % self.type_depense.lower()
                        second_code = "hr.bash.depense.register"
                    # sequence_code = "hr.bash.depense.%s" % self.type_depense.lower()
                    rec.name = self.env['ir.sequence'].search([('company_id', '=', comp)]).next_by_code(sequence_code)

        else:
            raise Warning('On ne peut pas effectuer un paiement de 0 FCFA Veuillez Cochez les Projets à payer')
            # return {'warning': {'title':'Alerte Message','message':'On ne peut pas effectuer un paiement de 0'}}
        # return True
    
    def action_valide_depense3(self,justification):
        invoice = self.env['caisse_depense.project']
        m_payment = self.env['hr.project_ouvert_lines']
        payment_line = self.env['account.payment']
        inv = []
        dc = 0
        amount = 0
        truth = [val.selection for val in self.project_ouvert_ids if val.amount != 0.0]
        if True in truth:
            dc = dc +1
        if dc >= 1:
        # if self.amount != 0.0:
            # end = m_payment.search([('selection','=',True),('project_id.en_paiement','=',False)])
            end = self.project_ouvert_ids
            for invoice in end:
                if invoice.selection == True and invoice.project_id.en_paiement == False:
                    amount += invoice.amount
                    invoice.project_id.write({'en_paiement': True})
                    invoice.project_id.write({'bash_project_id':self.id})
                    invoice.write({'selection': False})
                    inv = self.account_payment_line2(invoice.project_id)
                    payement = payment_line.create(inv)

            self.write({'en_paiement': 'valide'})
            if self.type_depense != 'bp':
                self.write({'state': 'valide'})
                self.write({'state': 'caisse'})
            else:
                
                employer=self.liste_employer()
                id_encaisseur=self.encaisseur_id.id
                
                if self.type_depense == 'bp' and id_encaisseur in employer:
                    self.write({'state': 'valide'})
                    self.env['rapport.acheteur'].create({
                            'bp_id':self.id,
                            'statut':"draft",
                            'justification':justification,
                            'justif_value':True
                            })
                else:
                    self.write({'state': 'valide'})    
            self.write({'amount': amount})
            rec = self
            if not rec.name:
                if self.type_depense:
                    comp = self.env.user.company_id.id
                    sequence_code = ''
                    second_code = ''
                    # sequence_code = "hr.bash.depense.%s" % self.type_depense.lower()
                    if self.type_depense == "bp":
                        sequence_code = "hr.bash.depense.bp"
                        second_code = "hr.bash.depense.register"
                        rec.register_seq = self.env['ir.sequence'].search([('company_id','=',comp)]).next_by_code(second_code)
                    elif self.type_depense == "op":
                        sequence_code = "hr.bash.depense.op"
                    else:
                        sequence_code = "hr.bash.depense.%s" % self.type_depense.lower()
                        second_code = "hr.bash.depense.register"
                    # sequence_code = "hr.bash.depense.%s" % self.type_depense.lower()
                    rec.name = self.env['ir.sequence'].search([('company_id', '=', comp)]).next_by_code(sequence_code)

        else:
            raise Warning('On ne peut pas effectuer un paiement de 0 FCFA Veuillez Cochez les Projets à payer')
            # return {'warning': {'title':'Alerte Message','message':'On ne peut pas effectuer un paiement de 0'}}
        # return True
        
        
        
    def cancel3(self):
            invoice = self.env['caisse_depense.project']
            amount = 0
            if self.nom_projet_ids:
                invoice_ids = self.nom_projet_ids
            # invoice_ids = invoice.search([('nom', '=', self.nom_projet), ('state', '=', 'approved'), ('en_paiement', '=', True)])

            elif self.initiateur_id:
                invoice_ids = invoice.search([('employee_id', '=', self.initiateur_id.id), ('state', '=', 'approved'), ('en_paiement', '=', True)])
            else:
                invoice_ids = invoice.search([('encaisseur_id', '=', self.encaisseur_id.id), ('state', '=', 'approved'),('en_paiement','=', True)])

            for invoice in invoice_ids:
                invoice.write({'en_paiement': False})
                invoice.write({'bash_project_id': False})
                self.write({'amount':amount})
                

            for i in self.project_ouvert_ids:
                i.write({'selection': False})

            for rec in self:
                rec.write({"state":"draft"})
                
                employer=[]
                liste_acheteur=self.env['caisse.acheteur'].search([],[])
                for values in liste_acheteur:
                    for personne in values:
                        if personne.encaisseur_id not in employer:
                            employer.append(personne.encaisseur_id.id)
                if self.type_depense == 'bp' and self.encaisseur_id.id in employer:
                    self.env['rapport.acheteur'].search([('bp_id','=',rec.id)],[]).unlink() 
                employer.clear() 

                # if rec.type_depense == 'bp' and rec.encaisseur_id.name=="Tchoupou Guillaume":
                #         self.env['rapport.acheteur'].searcch([('bp_id','=',rec.id)],[]).unlink() 
                        
                rec.payment_lines.unlink()
                rec.payment_lines = [(5,0,0)]

    @api.model
    def liste_employer(self):
        employer=[]
        employer.clear()
        liste_acheteur= self.env['caisse.acheteur'].search([],[])
        for values in liste_acheteur: 
            for personne in values:
                if personne.encaisseur_id not in employer:
                    employer.append(personne.encaisseur_id.id)
        return employer
    
    @api.model
    def check_permission(self,id):
        
        nbre_jour= self.env['caisse.acheteur'].search([('encaisseur_id','=',id)],[]).nbr_permis
        permission1= self.check_date(id,nbre_jour) 
       # nbre_bp = len(self.env['rapport.acheteur'].search([("encaisseur_id","=",id),("statut","in",("draft","bigining"))]))
        permission=3
        print("entrer dans la fonction des d'essaie")
        if permission1 > 0:
            permission=0
            print("entrer dans un 0000000")
        else:
            permission=1 
            print("entrer dans un 1111")
        return permission
    
    @api.model
    def check_date(self,id,jour):
        value=0   
        date_now= datetime.today().strftime('%Y-%m-%d')
        req=self.env['caisse_depense_rapport.bpjournalier'].search([("encaisseur_id","=",id),("statut","in",("draft","bigining"))])
        if req:
            for rapport in req:
                for elt in rapport:
                    new_date= elt.create_date + timedelta(days=jour)
                    new_date2=new_date.strftime('%Y-%m-%d')
                    print("new date",new_date)
                    print("date du jour",date_now) 
                    if  datetime.strptime(date_now, "%Y-%m-%d")  >= datetime.strptime(new_date2, "%Y-%m-%d") :
                        value +=1  
        return value 
                
        

    @api.multi
    def call_wizard(self):
        print ("call wizard fucntion")
        wizard_form = self.env.ref('caisse_depense_rapport.action_wizard_bp', False)
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
   
   
    def paiement_rbp_2(self):
        inv = []
        pay = self.env['account.payment']
        nn=""
        # self.amount = self.object_amount   
        # self.write({'amount': self.object_amount})
        for i in self.bp1_ids:
            inv = self.building(i)
            pay.create(inv)
        rec = self
        if not rec.name:
            sequence_code = 'hr.bash.depense.rbp'
            comp = self.env.user.company_id.id
            nn = self.env['ir.sequence'].search([('company_id','=',comp)]).with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
            rec.name = nn
            
        if self.state1 == "draft":
            self.write({'state1':'direction'})
            for rbp in self.bp1_ids:
                nom=rbp.bp_id.name
                v_name=nom.strip()
                id=self.env['rapport.acheteur'].search([('name','=',v_name)],[]).id
                id2=self.env['caisse_depense_rapport.bpjournalier'].search([('name','=',v_name)],[]).id 
                
                if id2:
                    self.env['caisse.bpjournalier.reste'].create({
                        'bonpro_id':id2,
                        'numero':nn,
                        'beneficiaire_id':self.beneficiaire_id.id,
                        'date_rbp':self.payment_date,
                        'montant':rbp.montant_retour,
                    })
                    
                if id:
                    self.env['caisse.vendeur.reste'].create({
                        'bonpro_id':id,
                        'numero':nn,
                        'beneficiaire_id':self.beneficiaire_id.id,
                        'date_rbp':self.payment_date,
                        'montant':rbp.montant_retour,
                    })
       
        return True
    
    def cancel_retour_2(self):
        amount = 0
        for record in self:
            for rbp in record.bp1_ids:
                nom=rbp.bp_id.name
                v_name=nom.strip()
                print("test function 2")
                id=self.env['rapport.acheteur'].search([('name','=',v_name)],[]).id
                id2=self.env['caisse_depense_rapport.bpjournalier'].search([('name','=',v_name)],[]).id 
                self.env['caisse.bpjournalier.reste'].search([('bonpro_id','=',id2)]).unlink()
                self.env['caisse.vendeur.reste'].search([('bonpro_id','=',id)]).unlink()
            record.bp1_ids.unlink()
            record.bp1_ids = [(5,0,0)]
            record.payment_lines.unlink()

        self.write({'state1':'draft'})
        self.write({'amount': amount})
        