from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError,Warning
from datetime import datetime,date

class Rapport_acheteur(models.Model):
    _name="rapport.acheteur"
    _inherit = ['mail.thread']
    _description = "rapport vendeur" 
    _rec_name = 'name'
    _order = 'id desc'
    
    # _sql_constraints = [('bp_id', 'unique (bp_id)', 'Ce bon provisoire est dèja selectionner ')]
    
    @api.constrains('facture_total') 
    def check_mount_total(self):
        for elt in self:
            if elt.amount < elt.facture_total:
                raise ValidationError("erreur!!!, contrôler les factures enregistrées")
            elif elt.facture_total< 0:
                raise ValidationError("erreur!!!, contrôler les factures enregistrées, total négative") 

       
   # bp_id=fields.Many2one('caisse_depense.project', string="Bon provisoire",required=True) 
    bp_id=fields.Many2one('account.bash.payment', string="Bon provisoire",required=True,readonly=True,store=True) 
    name = fields.Char(readonly=True,related='bp_id.name',store=True) 
    describe = fields.Char('Description',store=True,related='bp_id.describe')
    justification=fields.Text(string="Motif autorisation",store=True) 
    justif_value=fields.Boolean(string="Autoriser") 
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
    
    facture_ids=fields.One2many('rapport.acheteur.line','bonpro_id',ondelete='cascade',string="Liste factures")
    reste_ids=fields.One2many('caisse.vendeur.reste','bonpro_id',ondelete='cascade',string="Liste Restes")
    
    
    facture_total=fields.Float(string="Somme total",store=True,compute="onchange_total_facture")    
    reste_total=fields.Float(string="Reste",store=True,compute="onchange_total_reste")    
    
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
    reste_a_payer=fields.Float(string="Reste",store=True,compute="onchange_reste")  
    move = fields.Many2one('account.move',string="Piece comptable",related='bp_id.move',store=True)

    type = fields.Selection([
            ('payment_forni','Paiement fournisseur'),
            ('depense','Depense interne'),
            ('avoir_bp', 'Avoir BP'),
            ('baf','Avance fournisseur'),
            ('pmt','PMT'),
        ],related='bp_id.type',store=True)
    
   
  
        
    @api.depends('facture_ids.montant','facture_ids.numero')
    def onchange_total_facture(self):
        self.facture_total = 0
        self.facture_total = sum(val.montant for val in self.facture_ids)

    @api.depends('reste_ids.montant','reste_ids.numero')
    def onchange_total_reste(self):
        self.reste_total = 0.0
        self.reste_total = sum(val.montant for val in self.reste_ids)
        
    @api.depends('facture_total','reste_total')
    def onchange_reste(self):
        for bp in self:
            bp.reste_a_payer = bp.amount-(bp.facture_total + bp.reste_total)
        
    
    
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
    @api.multi
    def cancel(self):
        for bon in self:
                bon.statut="draft" 
                # rapport=self.env['rapport.acheteur'].search([('bp_id','=',bon.bp_id.id)])
                # for bp in rapport:
                #     bp.statut="draft"
                
    def get_total_amount(self):
        total_amount = 0.0
        req=self.env['rapport.acheteur'].search([],[])
        for elt in req:
            for value in elt:
                total_amount +=elt.amount
        
        print("total",total_amount) 
        return total_amount
           
               
class Rapport_acheteur_line(models.Model):
    _name = 'rapport.acheteur.line'
    _inherit = ['mail.thread']
    _description = "rapport"
    _rec_name = 'name'
    _order = 'id desc'
            
    name=fields.Char(string="nom")
    bonpro_id=fields.Many2one('rapport.acheteur',string="Bp",readonly=True,store=True)
    montant=fields.Float(string="Montant", required=True,default=0.0)
    #total=fields.Float(string="Total", store=True, invisible="1")
    description=fields.Text(string="Description sur la facture")
    numero=fields.Char(String="No facture", required=True)
    #fs_facture=fields.Char(String="Fournisseur",invisible="1")
    date_f = fields.Date(string="Date",require=True,store=True,default=fields.Date.context_today,readonly=True) 
    date_fac = fields.Date(string="Date sur Facture",require=True,store=True,) 
    fournisseur_divers = fields.Char(string="Fournisseur Divers",store=True)
    partner_id = fields.Many2one('res.partner', string='Fournisseur',store=True,require=True)
    fournisseur_inconnu = fields.Boolean(string="Fournisseur Inconnu", compute="check_fournisseur",store=True,readonly=True,default=False) 
    
    
    @api.depends('partner_id')
    def check_fournisseur(self):
        for line in self:
            if line.partner_id.name=="Fournisseurs divers":
                self.fournisseur_inconnu=True
                
                
class Caisse_vendeur_reste_line(models.Model):
    _name = 'caisse.vendeur.reste'
    _inherit = ['mail.thread']
    _description = "reste"
    _rec_name = 'name'
    _order = 'id desc'
            
    name=fields.Char(string="nom")
    bonpro_id=fields.Many2one('rapport.acheteur',string="Bp Associé",readonly=True,store=True)
    montant=fields.Float(string="Montant du RBP", required=True,default=0.0)
    numero=fields.Char(String="No RBP",required=True) 
    date_rbp=fields.Date(string="Date Emission RBP",required=True)
    #nom_rbp=fields.Char(string="No RBP", required=True)# a retirer
    beneficiaire_id = fields.Many2one('hr.employee',store=True, string="Beneficiaire",Required=True)
    
    @api.constrains('montant')
    def check_reste(self):
        for reste in self:
            if reste.montant<0:
                raise ValidationError('le montant est inferieure a zéro')
            
class Acheteur_liste5(models.Model):
    _name ='caisse.acheteur'
    _inherit = ['mail.thread']
    _description = "acheteur"
    _rec_name = 'name'
    _order = 'id asc'
    
    _sql_constraints = [('Encaisseur', 'unique(encaisseur_id)', 'un employée ne peut être enregistrer deux fois dans la liste')]

    encaisseur_id=fields.Many2one('hr.employee',string='Encaisseur',required=True,store=True)
    nbr_permis=fields.Integer(string="Nombre de BP permis",required=True)
    name=fields.Char(string="Nom")  