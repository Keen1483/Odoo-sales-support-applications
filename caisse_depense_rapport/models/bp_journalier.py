# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError,Warning
from datetime import datetime,date

class Caisse_depense_rapport(models.Model):
    _name = 'caisse_depense_rapport.bpjournalier'
    _inherit = ['mail.thread']
    _description = "rapport bon provisoire"
    _rec_name = 'name'
    _order = 'id desc'

    # # _sql_constraints = [('bp_id', 'unique (bp_id)', 'Ce bon provisoire est dèja selectionner ')]  
    
    @api.constrains('facture_total') 
    def check_mount_total(self):
        for elt in self:
            if elt.amount < elt.facture_total:
                raise ValidationError("erreur!!!, contrôler les factures enregistrées")
            elif elt.facture_total< 0:
                raise ValidationError("erreur!!!, contrôler les factures enregistrées, total négative") 
            
    # @api.constrains('facture_total','reste_total','garder') 
    # def check_amount_garder(self):
    #     for elt in self:
    #         if elt.amount < elt.facture_total + elt.reste_total + elt.garder:
    #             raise ValidationError("erreur!!!, contrôler les factures enregistrées ou le retours du bp ou la somme gardé")
    #         elif elt.facture_total + elt.reste_total + elt.garder< 0:
    #             raise ValidationError("erreur!!!, contrôler les factures enregistrées ou le retours du bp ou la somme gardé, total négative") 


       
   # bp_id=fields.Many2one('caisse_depense.project', string="Bon provisoire",required=True) 
    bp_id=fields.Many2one('account.bash.payment', string="Bon provisoire",required=True,readonly=True,store=True) 
    name = fields.Char(readonly=True,related='bp_id.name',store=True) 
    describe = fields.Char('Description',store=True,related='bp_id.describe')
    encaisseur_id = fields.Many2one('hr.employee',store=True, string="Encaisseur",related='bp_id.encaisseur_id')
    encaisseur2_id = fields.Many2one('res.partner',store=True, string="Encaisseur",related='bp_id.encaisseur2_id')
    initiateur_id = fields.Many2one('res.users',store=True, string="Initiateur",related='bp_id.initiateur_id')
    beneficiaire_id = fields.Many2one('hr.employee',store=True, string="Beneficiaire",related='bp_id.beneficiaire_id')
    beneficiaire2_id = fields.Many2one('res.partner',store=True, string="Beneficiaire",related='bp_id.beneficiaire2_id')
    beneficiaire = fields.Char(string='Beneficiaire',store=True,related='bp_id.beneficiaire')
    payment_lines = fields.One2many('account.payment', 'payment_id', string='factures',related='bp_id.payment_lines')
    nom_projet = fields.Char("No Reference Projet",store=True,related='bp_id.nom_projet')
    # nom_projet_ids = fields.Many2many('caisse_depense.project',string="No Reference Projet",store=True,related='bp_id.nom_projet_ids')
    nom_op = fields.Char(string='Reference OP/BP',related='bp_id.nom_op')
    project_ouvert_ids = fields.One2many('hr.project_ouvert_lines','bash_id',string="Projets Approuvés",related='bp_id.project_ouvert_ids')
    Date_jour=fields.Date(string="Date du jour", default=fields.Date.context_today )
    en_justif = fields.Boolean(string = 'En Justif',related='bp_id.en_justif',store=True)
    justif_id = fields.Many2one('caisse_depense.justif_bp',string="justif",related='bp_id.justif_id',store=True)
    state_justif = fields.Char(string="Statut Justif",related='bp_id.state_justif',store=True)
    is_justify = fields.Char(string='Est Justifié',related='bp_id.is_justify',store=True)

    register_seq = fields.Char(string='Sequence Classeur',related='bp_id.register_seq',store=True)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('valide', 'Valide'),
        ('controle_bp', 'Controle_BP'),
        ('direction', 'Direction'),
        ('caisse', 'Caisse'),
        ('controle', 'Controle'),
        ('verification', 'Verification'),
        ('comptabilité', 'Comptabilité'),
        ('justifier','Justifier'),
        ('reconciled', 'Reconciled')
    ],related='bp_id.state',store=True)
    type_depense = fields.Selection([
        ("op", "OP"),
        ("bp", "BP"),
        
    ], string="Type de Decaissement",store=True,related='bp_id.type_depense')
    
    other_describe = fields.Char('Description supplementaire', store=True,related='bp_id.other_describe')
    
    statut = fields.Selection([
        ('draft', 'A justifier'),
        ('bigining', 'En cours'),
        ('justify', 'Justifié') 
    ], string='Status', store=True)
    
    
    facture_ids=fields.One2many('caisse.bpjournalier.line','bonpro_id',ondelete='cascade',string="Liste factures")
    reste_ids=fields.One2many('caisse.bpjournalier.reste','bonpro_id',ondelete='cascade',string="Liste Restes")
    garder_ids=fields.One2many('retour.garder.line','rapport_id',ondelete='cascade',string="Garder") 
    
    facture_total=fields.Float(string="Somme total",store=True,compute="onchange_total_facture")    
    reste_total=fields.Float(string="Reste",store=True,compute="onchange_total_reste")    
    reste_a_payer=fields.Float(string="Reste",store=True,compute="onchange_reste")    
    
    invoice_lines = fields.One2many('account.payment_line','bash_id',related='bp_id.invoice_lines',store=True,string='Toutes Factures à Payées')
    amount_provider = fields.Float(string="Montant Calculé",related='bp_id.amount_provider',store=True)
    journal_id = fields.Many2one('account.journal', string='Journal de paiement',store=True,related='bp_id.journal_id' )
    company_id = fields.Many2one('res.company', string='Société',store=True, related='bp_id.company_id')
   
    partner_type = fields.Selection([('customer', 'Customer'), 
                                     ('supplier','Vendor')],related='bp_id.partner_type',store=True )
    
    new_amount = fields.Char(string="Nouveau Montant",store=True,related='bp_id.new_amount')
    new_pay_id = fields.Many2one('account.payment',string="Avance Paiement",store=True,related='bp_id.new_pay_id')
    # new_pay_id = fields.Many2one('account.payment',string="Avance Paiement")
    avanced = fields.Boolean(string="Avance",related='bp_id.avanced',store=True)    
    partner_id = fields.Many2one('res.partner', string='Fournisseur',store=True,related='bp_id.partner_id')
    document_line_id = fields.Many2one('gestion.document.line', string='Document',store=True,related='bp_id.document_line_id')
    # banque_id = fields.Many2one('account.journal',string='Banque')
    banque2_id = fields.Many2one('res.bank',string='Banque',related='bp_id.banque2_id',store=True)
    banque3_id = fields.Char(string='Nom Compte Bancaire',related='bp_id.banque3_id',store=True)

    # amount_calculed = fields.Float(string='Montant Facture BPF',store=True)
    # dif_facture = fields.Float(string="Difference",store=True)

    communication = fields.Char(string='Memo',related='bp_id.communication',store=True)
    payment_date = fields.Date(string='Date',related='bp_id.payment_date',store=True)
    # move_line_ids = fields.One2many('account.move.line', 'payment_id' )
    
    currency_id = fields.Many2one('res.currency', string='Devise',related='bp_id.currency_id',store=True)
    amount = fields.Monetary(string='Montant du paiement',related='bp_id.amount',store=True)
    sequent = fields.Many2one('ir.sequence',string='Sequence',related='bp_id.sequent',store=True)
    # observation = fields.Text(string="Observation")
    imprime = fields.Char(string='Impression',related='bp_id.imprime',store=True)
    fournisseur_divers = fields.Char(string="Fournisseur Divers",related='bp_id.fournisseur_divers',store=True)
    no_cheque = fields.Char(string="No Cheque",related='bp_id.no_cheque',store=True)
    en_lettre = fields.Char(string="En Lettre",related='bp_id.en_lettre',store=True)

    total1 = fields.Monetary('Total1',related='bp_id.total1',store=True)
    total2 = fields.Monetary('Total2',related='bp_id.total2',store=True)
    total3 = fields.Monetary('balance',related='bp_id.total3',store=True)
    total4 = fields.Monetary('Total4',related='bp_id.total4',store=True)
    nbl = fields.Integer('Nombre de Ligne',related='bp_id.nbl',store=True)
    montant_avoir = fields.Monetary('Montant Avoir',related='bp_id.montant_avoir',store=True)
    
    destination_cheque_id = fields.Many2one('account.cheque_destination',string='Destination Chèque',related='bp_id.destination_cheque_id',store=True)
    justificatif = fields.Char(string="Justicatif",related='bp_id.justificatif',store=True)

    move = fields.Many2one('account.move',string="Piece comptable",related='bp_id.move',store=True)
    garder =fields.Float(string='Gardé',default=0.0,compute="onchange_total_garder")
    delais=fields.Char(strings="Delais", compute="onchange_delais")
    delais_garder=fields.Char(strings="Delais", compute="onchange_delais2")
    end_date=fields.Date(string="end date")

    # type = fields.Selection([
    #         ('payment_forni','Paiement fournisseur'),
    #         ('depense','Depense interne'),
    #         ('avoir_bp', 'Avoir BP'),
    #         ('baf','Avance fournisseur'),
    #         ('pmt','PMT')
    #     ],related='bp_id.type',store=True)
    type = fields.Char(string="type",default="BP",store=True)
    
   
  
    @api.depends('garder_ids.amount_garder','garder_ids.total')
    def onchange_total_garder(self):
        for bp in self:
            garder = sum(val.amount_garder for val in bp.garder_ids)    
            retirer = sum(val.total for val in bp.garder_ids)   
            bp.garder= garder - retirer 
            
            
            
    @api.depends('facture_ids.montant','facture_ids.numero')
    def onchange_total_facture(self):
        self.facture_total = 0
        self.facture_total = sum(val.montant for val in self.facture_ids)

    @api.depends('reste_ids.montant','reste_ids.numero')
    def onchange_total_reste(self):
        for bp in self:
            bp.reste_total = sum(val.montant for val in bp.reste_ids)
    
    @api.depends('facture_total','reste_total')
    def onchange_reste(self):
        for bp in self:
            bp.reste_a_payer = bp.amount-(bp.facture_total + bp.reste_total)
            
    @api.depends('delais')
    def onchange_delais(self):
        dt=self.change_date()
        if dt != None:
            end_date= datetime.strptime(dt,'%Y-%m-%d')
            for bp in self:
                t= bp.create_date.strftime('%Y-%m-%d') 
                date_satrt=datetime.strptime(t,'%Y-%m-%d')
                d= str(date_satrt - end_date) 
                if type(d[2]) == str:
                    bp.delais = d[1]
                else:
                    bp.delais = d[0:2]
        else:
            for bp in self:
                bp.delais="0"
                
    def format_date(self,date):
                date1=date.strftime('%Y-%m-%d')
                date2=datetime.strptime(date1,'%Y-%m-%d') 
                year = str(date2.year)
                month = str(date2.month)
                day = str(date2.day)  
                if len(day) == 1:
                    day = '0' + day
                if len(month) == 1:
                    month = '0' + month
                result = day + '.' + month + '.' + year[2] + year[3]
                return result
                       
    @api.depends('delais_garder')
    def onchange_delais2(self): 
        dt=self.change_date2()
        if dt != None:
            end_date= datetime.strptime(dt,'%Y-%m-%d')
            for bp in self:
                t= bp.create_date.strftime('%Y-%m-%d') 
                date_satrt=datetime.strptime(t,'%Y-%m-%d')
                d= str(date_satrt - end_date) 
                if type(d[2]) == str:
                    bp.delais_garder = d[1]
                else:
                    bp.delais_garder = d[0:2]
        else:
            for bp in self:
                bp.delais_garder="0"   
                
    @api.model
    def change_date(self):
       for elt in self: 
            req= self.env['caisse.bpjournalier.reste'].search([('bonpro_id','=',elt.id)],limit=1,order="id desc").create_date
            if req:
                return  req.strftime('%Y-%m-%d')  
    
    @api.model
    def change_date2(self):
       for elt in self: 
            req= self.env['retour.garder.line'].search([('rapport_id','=',elt.id)],limit=1,order="id desc").create_date
            if req:
                return  req.strftime('%Y-%m-%d')  
    
    def __datetime(date_start):
        return datetime.strptime(date_start, '%d/%m/%Y')
    
    @api.onchange('bp_id')
    def onchange_bp_id(self):
       obj=self.search([])
       available_ids=[]        
       for elt in obj: 
           available_ids.append(elt.bp_id.id)
       return {'domain':{'bp_id':[('id','not in',available_ids),('type_depense','=','bp'),('state','=','caisse')]}}
    
    @api.multi   
    def check_statut(self):
       for bon in self:
           if bon.reste_a_payer ==bon.amount:
               bon.statut="draft" 
           elif bon.reste_a_payer < bon.amount and bon.reste_a_payer > 200:
                rapport=self.env['rapport.acheteur'].search([('bp_id','=',bon.bp_id.id)])
                for bp in rapport:
                    bp.statut="bigining" 
                bon.statut="bigining"
           elif bon.reste_a_payer < bon.amount and bon.reste_a_payer <= 200:
                rapport=self.env['rapport.acheteur'].search([('bp_id','=',bon.bp_id.id)])
                for bp in rapport:
                    bp.statut="justify"
                bon.statut="justify"
           for garde in bon.garder_ids:
                if garde.state=="draft":
                   garde.state=="garde"  
                    
                
    
    @api.multi
    def cancel(self):
        for bon in self:
                bon.statut="draft" 
                rapport=self.env['rapport.acheteur'].search([('bp_id','=',bon.bp_id.id)])
                for bp in rapport:
                    bp.statut="draft" 
                    
    #fonction d'ajout dans un fichier pdf 
    def post(self):
        

        bank_statement_line= self.env['account.bank.statement.line'].search([('payment_ids','=',False)])
        value = []
        for bank_statement_lines in bank_statement_line:
            if bank_statement_lines.appro_id:
                if abs(bank_statement_lines.appro_id.amount) != abs(bank_statement_lines.amount):
                    val = {
                        'id appro' : bank_statement_lines.appro_id.id,
                        'nom' : bank_statement_lines.appro_id.name,
                        'montant' : bank_statement_lines.appro_id.amount,
                        'creer_par' : bank_statement_lines.appro_id.create_uid.name,
                        'creer_le' : bank_statement_lines.appro_id.create_date.strftime('%d.%m.%y'),
                        'beneficiere_appro' : bank_statement_lines.appro_id.beneficiaire_id.name,
                        'initiateur_appro' : bank_statement_lines.appro_id.initiateur_id.name,
                        'reference_piece'  : bank_statement_lines.appro_id.ref,
                        'date_piece' : bank_statement_lines.appro_id.date.strftime('%d.%m.%y'),
                        'libelle'  : bank_statement_lines.appro_id.libelle,
                        'piece comptable'  : bank_statement_lines.appro_id.move_id.name,
                        'agence'  : bank_statement_lines.appro_id.agence_id.name,
                        'type appro'  : bank_statement_lines.appro_id.type,

                        'id caisse' : bank_statement_lines.id,
                        'montant_caisse' : bank_statement_lines.amount,
                        'appro_caisse' : bank_statement_lines.appro_id.name,
                        'creer_par_caisse' : bank_statement_lines.create_uid.name,
                        'creer_le_caisse' : bank_statement_lines.create_date.strftime('%d.%m.%y'),
                        'beneficiere caisse': bank_statement_lines.appro_id.beneficiaire_id.name,
                        'initiateur caisse': bank_statement_lines.appro_id.initiateur_id.name,
                        'libelle caisse': bank_statement_lines.name,
                        'reference_piece_caisse': bank_statement_lines.ref_piece,
                    }
                    value.append(val)
        print('value',len(value))
        print('value',value)
        return self.env.ref('caisse_depense.controle_caisse_id_report').report_action([], data={'value': value})
             
                    
                    
                    
                    
                    
                    
                    
    
class Caisse_depense_rapport_line(models.Model):
    _name = 'caisse.bpjournalier.line'
    _inherit = ['mail.thread']
    _description = "rapport"
    _rec_name = 'name'
    _order = 'id desc'
            
    name=fields.Char(string="nom")
    bonpro_id=fields.Many2one('caisse_depense_rapport.bpjournalier',string="Bp",readonly=True,store=True)
    montant=fields.Float(string="Montant", required=True,default=0.0)
    #total=fields.Float(string="Total", store=True, required=True,invisible="1")
    reste=fields.Float(string="Reste", default=0.0,invisible="1")
    description=fields.Text(string="Description sur la facture")
    numero=fields.Char(String="Facture", required=True)
    fs_facture=fields.Char(String="Fournisseur sur le facture",invisible="1")
    date_f = fields.Date(string="Date du jour",require=True,store=True,default=fields.Date.context_today,readonly=True) 
    date_fac = fields.Date(string="Date sur Facture",require=True,store=True,) 
    fournisseur_divers = fields.Char(string="Fournisseur Divers",store=True)
    partner_id = fields.Many2one('res.partner', string='Fournisseur',store=True,require=True)
    fournisseur_inconnu = fields.Boolean(string="Fournisseur Inconnu", compute="check_fournisseur",store=True,default=False) 
    #fournisseur_inconnu = fields.Boolean(string="Fournisseur Inconnu", store=True,default=False) 
    
    
   
    # @api.depends('partner_id')
    # def check_fournisseur(self):
    #     for line in self:
    #         if line.partner_id.name=="Fournisseurs divers":
    #             self.fournisseur_inconnu=True
                
                
    # @api.onchange('fournisseur_inconnu')
    # def check_fournisseur(self):
    #     for line in self:
    #         if line.partner_id:
    #             if line.partner_id.name=="Fournisseurs divers":
    #                 self.fournisseur_inconnu=True
    
    
class Caisse_depense_reste_line(models.Model):
    _name = 'caisse.bpjournalier.reste'
    _inherit = ['mail.thread']
    _description = "reste"
    _rec_name = 'name'
    _order = 'id desc'
            
    name=fields.Char(string="nom")
    bonpro_id=fields.Many2one('caisse_depense_rapport.bpjournalier',string="Bp Associé",readonly=True,store=True)
    montant=fields.Float(string="Montant du RBP", required=True,default=0.0)
    numero=fields.Char(String="No RBP",required=True) 
    date_rbp=fields.Date(string="Date Emission RBP",required=True)
    #nom_rbp=fields.Char(string="No RBP")# a retirer
    beneficiaire_id = fields.Many2one('hr.employee',store=True, string="Beneficiaire",Required=True)
    
    @api.constrains('montant')
    def check_reste(self):
        for reste in self:
            if reste.montant<0:
                raise ValidationError('le montant est inferieure a zéro')
  
    
   
        
    

        
        
   