from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError,Warning
from datetime import datetime,date


class Retour_garder(models.Model):
    
    _name="retour.garder"
    _description="Retour garder"
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _order = 'id desc'
    
    name=fields.Char(string="name", index=True,default = lambda self: _('Nouveau'))
    initiateur_id = fields.Many2one('res.users',store=True, string="Initiateur",required=True)
    describe = fields.Char('Description',store=True)
    encaisseur_id = fields.Many2one('hr.employee',store=True, string="Encaisseur",required=True)
    beneficiaire_id=fields.Many2one('hr.employee',store=True, string="Encaisseur", required=True)
    # journal_id=fields.Many2one('account.journal',string="Journal", required=True) 
    date_garder=fields.Date(string="Date",default=fields.Date.context_today, required=True)
    garde_ids=fields.One2many('retour.garder.line','garder_id', string="liste de bp garder")
    state=fields.Selection([
        ('draft', 'Brouillon'),
        ('valide', 'Validé')
    ],default="draft",track_visibility='onchange')
    
    def cancel_Garder(self):
        if self.state == "valide":
            for record in self:
                for bp in record.garde_ids:
                    id=bp.bp_id.id
                    montant=bp.amount_garder
                    id2=self.env['caisse_depense_rapport.bpjournalier'].search([('bp_id','=',id)],[])
                    for v_caisse in id2:
                        v_caisse.garder = v_caisse.garder - montant 
            self.write({'state':'draft'})
        return True
                       
                        
    # @api.depends('garde_ids.nature')           
    # def get_reste_garde(self):
    #     caisse=0.0
    #     req=self.env['retour.garder.line'].search([('bp_id','=',self.garde_ids.bp_id.id)],order="id desc",limit =1)  
    #     print("req est", req)
    #     if self.garde_ids.nature=="retire":
    #         for elt1 in req:
    #             for value in elt1:
    #                 caisse= value.caisse_bp 
    #             self.garde_ids.reste_garde=caisse 
    #     elif self.garde_ids.nature=="garde":
    #         for elt1 in req:
    #             for value in elt1:
    #                 caisse= value.caisse_bp 
    #             self.garde_ids.reste_garde=caisse
        
        
    def paiement_garder(self):
        if self.state == "draft":
    
            for record in self:
                for garder in record.garde_ids:
                    id=garder.bp_id.id
                    garder.state="garde"
                    montant=garder.amount_garder
                    id2=self.env['caisse_depense_rapport.bpjournalier'].search([('bp_id','=',id)],[])
                   # for v_caisse in id2:
                       # v_caisse.garder = v_caisse.garder + montant
            self.write({'state':'valide'})
        return True 
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('Nouveau')) == _('Nouveau'):
            sequence_code = 'hr.bash.retour.garder'
            comp = self.env.user.company_id.id
            vals['name'] = self.env['ir.sequence'].search([('company_id', '=', comp)]).next_by_code(sequence_code) or _('Nouveau')
        return super(Retour_garder, self).create(vals)
    
class Retour_garder_line(models.Model):
    _name="retour.garder.line"
    _description="reste garder"
    
    
    @api.constrains('caisse_bp')
    def check_amount_garder(self):
        for elt in self:
            if elt.caisse_bp > elt.amount_bd:
                raise ValidationError('Le montant gardé est supérieure au montant du bp.')
            elif elt.caisse_bp < 0:
                raise ValidationError('Ce BP a un solde égale à zéro, vous pouvez uniquement gardé.')
            
                
    @api.model
    def _devise(self):
        return self.env['res.currency'].search([('name', '=', 'XAF')])
    
    @api.constrains('total')
    def chek_total(self):
        for elt in self:
            if elt.total > elt.amount_garder:
                raise ValidationError('La somme des retraits est supérieure au montant gardé') 
            
    

    currency_id = fields.Many2one('res.currency', string='Devise', required=True, default=_devise)
    name=fields.Char(string="Name",default = lambda self: _('Nouveau'), index=True )
    describe = fields.Char('Description',store=True, required=True)
    garder_id=fields.Many2one('retour.garder',string="Retour", required=True)
    name_garder=fields.Char(string="Piece garder", related='garder_id.name')
    bp_id=fields.Many2one('account.bash.payment', string="Bon provisoire",required=True) 
    amount_bd =fields.Monetary(string='Montant du BP',related='bp_id.amount')    
    bp_description =fields.Char('Description',store=True,related='bp_id.describe')  
    amount_garder= fields.Float(string="Montant Garder",store=True) # compute="get_amount_garder", 
    amount_retirer= fields.Float(string="Montant Retirer",store=True) 
    total= fields.Float(string="Total",store=True,default=0.0, required=True)
    date_g=fields.Date(string="date", default=fields.Date.context_today)
    # retrait_ids=fields.One2many('retrait.garder','retour_id',string='Retrait') 
    state=fields.Selection([
        ('draft', 'Brouillon'),
        ('garde', 'Gardé'),
        ('valide', 'validé')
    ],default="draft",track_visibility='onchange')
    rapport_id=fields.Many2one('caisse_depense_rapport.bpjournalier', string="Rapport",compute="onchange_rapport",store=True)
    montant=fields.Float(string="Montant",default=None)
    reste_garde=fields.Float(string="Reste", store=True) #compute="check_nature_bp",
    nature=fields.Selection([
        ('retire', 'Retrait'),
        ('garde', 'Gardé')
    ],track_visibility='onchange',required=True)
    caisse_bp=fields.Float(string='Caisse BP',store=True)  #compute="get_caisse",
    garder=fields.Boolean(string="garder",compute="check_nature_bp", store=True)
    retirer=fields.Boolean(string="retirer", compute="check_nature_bp", store=True)
    
    @api.depends('bp_id')
    def onchange_rapport(self):
        for elt in self:
            bp = elt.bp_id.id
            id = self.env['caisse_depense_rapport.bpjournalier'].search([("bp_id","=",bp)]).id
            if id:
                elt.rapport_id=id
            
   
            
    
    #pour empécher la repetition des numero de bp
    # @api.depends("nature","montant")
    # def get_amount_garder(self):
    #     for line in self:
    #         if line.nature=="garde":
    #             line.amount_garder=line.montant 
    #         elif line.nature=="retire":
    #             line.amount_garder=0.0
    
    
   
                        
    @api.onchange('bp_id')
    def get_reste_garde(self):
        caisse=0.0
        for elt in self:
            if elt.bp_id: 
                print("onchange bp pour test aprofondi")
                req=self.env['retour.garder.line'].search([('bp_id','=',elt.bp_id.id)],order="id desc",limit =1)  
                print("req est", req)
               
                for elt1 in req:
                    for value in elt1:
                        caisse= value.caisse_bp 
                elt.reste_garde=caisse 
                        
               
    @api.onchange('montant','nature')  
    def  get_caisse_onchange(self):
        caisse=0.0  
        print("eentrer dns la fonction de test de bp")
        for elt in self:
            req=self.env['retour.garder.line'].search([('bp_id','=',elt.bp_id.id)],order="id desc",limit =1)  
            print("req est", req)
            if req:
                if elt.nature:
                    if elt.montant:
                        if self.nature=="garde":
                            for elt1 in req:
                                for line in elt1:
                                    caisse= elt.montant + line.caisse_bp 
                            elt.caisse_bp= caisse 
                            elt.amount_garder=elt.montant
                            elt.amount_retirer=0.0
                        elif self.nature=="retire":
                            for elt1 in req:
                                for line in elt1:
                                    caisse=line.caisse_bp 
                            elt.caisse_bp= caisse - self.montant
                            elt.amount_retirer=elt.montant
                            elt.amount_garder=0.0
            else:
                if elt.nature:
                    if elt.montant:
                        if self.nature=="garde":  
                            elt.caisse_bp= elt.montant
                            elt.amount_garder=elt.montant
                            elt.amount_retirer=0.0
                            print('entrer dans la fonction 2')
                        elif self.nature=="retire":
                            elt.caisse_bp= -elt.montant
                                
    
    #remplir la caisse lié a u, bp 
    
    @api.depends('montant')
    def get_caisse(self):
            caisse=0.0
            req=self.env['retour.garder.line'].search([('bp_id','=',self.bp_id.id)],order="id desc",limit =1) 
            print("req est", req)
            
            if self.nature=="garde":
                    for elt in req:
                        for line in elt:
                            caisse= self.montant + line.caisse_bp 
                    self.caisse_bp= caisse 
            elif self.nature=="retire":
                    
                    for elt in req:
                        for line in elt:
                            caisse=line.caisse_bp 
                    self.caisse_bp= caisse - self.montant
            
    @api.depends('nature')
    def check_nature_bp(self):
        for  elt in self:
            if elt.nature=="retire":
                elt.retirer=True
            elif elt.nature=="garde":
                elt.garder=True
    
            
                
    @api.onchange('bp_id')
    def change_bp(self):
        obj=self.search([])
        req= self.env['caisse_depense_rapport.bpjournalier'].search([('statut','!=','justify')],[])
        bp=[]
        bps=[]
        for bon in obj:
            bps.append(bon.bp_id.id)
        for elt in req:
            for value  in elt:
                 bp.append(value.bp_id.id)
        return {'domain':{'bp_id':[('id','in',bp)]}}
    
    def paiement_garder(self):
        if self.state != "valide":
            
            for record in self:
                if record.total == record.amount_garder:
                    record.state='valide'
                else:
                    record.state='draft'
        elif self.state == "valide":
            self.write({'state':'draft'})   
        return True 
    
    @api.model
    def create(self,vals):
        
        if vals.get('name',_('Nouveau')) == _('Nouveau'):
            sequence_code = 'hr.bash.retour.garder.line'
            comp = self.env.user.company_id.id
            vals['name'] = self.env['ir.sequence'].search([('company_id', '=', comp)]).next_by_code(sequence_code) or _('Nouveau')
        return super(Retour_garder_line, self).create(vals)
    
    
class Retrait_garder(models.Model):
    _name="retrait.garder" 
    _description="gestion des retraits"
    
    
    initiateur_id = fields.Many2one('res.users',store=True, string="Initiateur",required=True)
    beneficiaire_id=fields.Many2one('hr.employee',store=True, string="Encaisseur", required=True)
    date_garder=fields.Date(string="Date",default=fields.Date.context_today, required=True)
    name=fields.Char(string="name", index=True,default = lambda self: _('Nouveau'))
    describe = fields.Char('Description',store=True)
    state=fields.Selection([
        ('draft', 'Brouillon'),
        ('valide', 'Validé')
    ],default="draft",track_visibility='onchange')
    retrait_ids=fields.One2many('retrait.garder.line','retrait_id',string="Retrait")
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('Nouveau')) == _('Nouveau'):
            sequence_code = 'hr.bash.retrait.garder'
            comp = self.env.user.company_id.id
            vals['name'] = self.env['ir.sequence'].search([('company_id','=', comp)]).next_by_code(sequence_code) or _('Nouveau')
        return super(Retrait_garder, self).create(vals)
    
    
    def paiement_garder(self):
        if self.state != "valide":
            for record in self:
                    record.state='valide'
                    for line in record.retrait_ids:
                        line.state="retire"
                        bp=line.bp_id.id  
                        req=self.env['retour.garder.line'].search([('bp_id','=',bp),('state','=','garde')],limit=1)
                        for ret_garder in req:
                            ret_garder.state="valide" 
                         
        elif self.state == "valide":
            self.write({'state':'draft'})   
        return True 


class Retrait_garder_line(models.Model):
    _name="retrait.garder.line" 
    _description="gestion des retraits" 
    
    @api.model
    def _devise(self):
        return self.env['res.currency'].search([('name', '=', 'XAF')])
    
    @api.constrains('montant_retrait','amount_garder')
    def check_montant(self):
        for elt in self:
            if elt.montant_retrait < 0:
                raise ValidationError('Le montant a rétirer ne peut pas être inférieure a 0')
            elif elt.montant_retrait > elt.amount_garder:
                raise ValidationError('Le montant a retirer ne peut pas être supérieure au monatant gardé')
    
    name=fields.Char(string="Nom")  
    retrait_id=fields.Many2one('retrait.garder',string="no retait", required=True)
    bp_id=fields.Many2one('account.bash.payment', string="Bon provisoire",required=True) 
    currency_id = fields.Many2one('res.currency', string='Devise', required=True, default=_devise)  
    amount_bd =fields.Monetary(string='Montant du BP',related='bp_id.amount',store=True)    
    bp_description =fields.Char('Description',store=True,related='bp_id.describe') 
    retour_id=fields.Many2one('retour.garder.line',string="No retour",required=True, compute="chek_retour")
    amount_garder= fields.Float(string="Montant Gardé",related="retour_id.amount_garder",store=True)
    describe_garder = fields.Char('Description',store=True)   # en cas de retour ici mettre un related avec retour_id 
    montant_retrait=fields.Float(string='Montant', required=True ) 
    state=fields.Selection([
        ('draft', 'Brouillon'),
        ('biging', 'En cours'),
        ('retire', 'Retiré')
    ],default="draft",track_visibility='onchange') 
    
    
    @api.onchange('bp_id')
    def change_bpid(self):
        obj=self.search([])
        req= self.env['retour.garder.line'].search([('state','=','garde')],[])
        bp=[]
        bps=[]
        for bon in obj:
            bps.append(bon.bp_id.id)
        for elt in req:
            for value in elt:
                bp.append(value.bp_id.id)
        return {'domain':{'bp_id':[('id','in',bp)]}}   
    
    
    @api.depends('bp_id')
    def chek_retour(self): 
        for elt in self:
            bp=elt.bp_id.id 
            req=self.env['retour.garder.line'].search([('bp_id','=',bp),('state','=','garde')],limit=1)
            for garde in req:
                elt.retour_id=garde.id   
    
    # def paiement_garder(self):
    #     if self.state != "retire":
    #         for record in self:
    #             record.state='retire'
    #             req=self.env['retour.garder.line'].search([('bp_id','=',record.bp_id.id),('state','=','garde')],limit=1)  
    #             for elt in req:
    #                elt.state=""  
      
    #     elif self.state == "retire":
    #         self.write({'state':'draft'})   
    #     return True 
                
                
     
    
    
    