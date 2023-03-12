# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date

import ast
import re


class BashPaymentReport(models.Model):
    _inherit = 'account.bash.payment'
    _description = 'Rapport des bash de paiement en pdf et xls'

    sent_to_print = fields.Boolean(compute='comp_invoices_lines_len')

    def comp_invoices_lines_len(self):
        if len(self.invoice_lines) > 0:
            self.sent_to_print = True
        else:
            self.sent_to_print = False

    # ### FUNCTION DE GENERATION DES RAPPORT PDF ET EXCEL ###
    def get_data(self):
        # LISTE DE DICTIONNAIRES DE BASH DE PAIEMENT
        result = []
        number_of_bash_selected = 0

        # TRANSFORME LES ARTICLES DE LA FACTURE EN UNE LISTE DE DICTIONNAIRE
        def articles(invoice_line_ids=[]):
            products = []
            if invoice_line_ids:
                for invoice_line in invoice_line_ids:
                    products.append({'name': invoice_line.product_id.product_tmpl_id.name})
                return products

        def periode(invoice_line_ids=[]):
            periodes = []
            if invoice_line_ids:
                for invoice_line in invoice_line_ids:
                    periodes.append({'name': invoice_line.periode})
                return periodes

        def compte(invoice_line_ids=[]):
            comptes = []
            if invoice_line_ids:
                for invoice_line in invoice_line_ids:
                    comptes.append({'name': invoice_line.account_id.code + ' ' + invoice_line.account_id.name})
                return comptes

        def tag(invoice_line_ids=[]):
            tags = []
            if invoice_line_ids:
                for invoice_line in invoice_line_ids:
                    for analytic_tag in invoice_line.analytic_tag_ids:
                        tags.append({'name': analytic_tag.name})
                return tags

        def donnees_fournisseur(donnees_multiple_ids=[]):
            data = {}
            i = 1
            if donnees_multiple_ids:
                for record in donnees_multiple_ids:
                    data[i] = record.date
                    i += 1
                return data

        def max_date(first, second):
            if first <= second:
                return second
            else:
                return first

        def min_date(first, second):
            if first >= second:
                return second
            else:
                return first

        def tri_max_date(dict_date={}):
            if dict_date:
                i = 1
                temp = dict_date[i]
                for val in dict_date:
                    if i < len(dict_date):
                        temp = max_date(temp, dict_date[val + 1])
                    else:
                        return temp
                    i += 1
            else:
                return None

        def tri_min_date(dict_date={}):
            if dict_date:
                i = 1
                temp = dict_date[i]
                for val in dict_date:
                    if i < len(dict_date):
                        temp = min_date(temp, dict_date[val + 1])
                    else:
                        return temp
                    i += 1
            else:
                return None

        # RECUPERATION DU RECORD COURANT
        current_bash = self.env['account.bash.payment'].search([('id', '=', self.id)])
        if current_bash:
            # TEST NOUVEAU PROJET DU 22/07/22
            if current_bash.payment_lines:
                for record in current_bash.payment_lines:
                    # RECUPERATION DES BASH QUI SONT EN STATUT OUVERT
                    # if current_bash.invoice_lines:
                    #     for record in current_bash.invoice_lines:
                    # print(record.invoice_id)
                    # RECUPERATION DES SELECTIONNES
                    # if record.selection and current_bash.state == 'caisse':
                    if current_bash.state == 'caisse':
                        date_bc = record.invoice_id.bc_multiple_ids[0].date if (
                                record.invoice_id.bc_multiple_ids and record.invoice_id.bc_multiple_ids[
                            0].date) else datetime(1, 1, 1, 0, 0).date()
                        date_bl = record.invoice_id.bl_multiple_ids[0].date if (
                                record.invoice_id.bl_multiple_ids and record.invoice_id.bl_multiple_ids[
                            0].date) else datetime(1, 1, 1, 0, 0).date()
                        date_brml = record.invoice_id.br1_manuel_ids[0].date if (
                                record.invoice_id.br1_manuel_ids and record.invoice_id.br1_manuel_ids[
                            0].date) else datetime(1, 1, 1, 0, 0).date()
                        date_brmc = record.invoice_id.br1_machine_ids[0].date if (
                                record.invoice_id.br1_machine_ids and record.invoice_id.br1_machine_ids[
                            0].date) else datetime(1, 1, 1, 0, 0).date()

                        date_bcomande = donnees_fournisseur(record.invoice_id.bc_multiple_ids)
                        date_blivraison = donnees_fournisseur(record.invoice_id.bl_multiple_ids)
                        date_brmuel = donnees_fournisseur(record.invoice_id.br1_manuel_ids)
                        date_brmchine = donnees_fournisseur(record.invoice_id.br1_machine_ids)

                        bc = tri_min_date(date_bcomande)
                        bl = tri_max_date(date_blivraison)
                        brml = tri_max_date(date_brmuel)
                        brmc = tri_max_date(date_brmchine)

                        dv = record.invoice_id.move_id.date

                        delai_dfa_brml = (record.invoice_id.date_invoice - brml) if brml else None
                        delai_bc_brml = (bc - brml) if bc and brml else None
                        delai_bl_brml = (bl - brml) if bl and brml else None
                        delai_brml_brml = (brml - brml) if brml and brml else None
                        delai_brmc_brml = (brmc - brml) if brmc and brml else None
                        delaitt_dv_brml = (dv - brml) if brml and dv else None

                        result.append({
                            # ### INFORMATIONS RELATIVES AU PREMIER RAPPORT ###

                            # Fournisseur
                            'partner': record.partner_id.name,
                            # Bash no
                            'bash_no': record.payment_id.name,
                            # Reglement
                            'rule': 'Esp' if record.invoice_id.esp else 'Chq',
                            # No Cheque
                            'no_cheque': record.payment_id.document_line_id.name,
                            # Journal
                            'journal': record.payment_id.journal_id.name,
                            # Bash date
                            'bash_date': record.payment_id.payment_date,
                            # Bash statut
                            'bash_status': record.payment_id.state,
                            # Bash nbr facture
                            # 'bash_nbr': record.bash_id.nbl,
                            # Bash montant
                            'bash_amount': record.payment_id.amount_provider,
                            # Bash crée le
                            'created_at': record.payment_id.create_date.date(),
                            # Bash crée par
                            'created_by': record.payment_id.create_uid.name,
                            # Bash Date MAJ
                            'updated_at': record.payment_id.write_date.date(),
                            # Bash MAJ par
                            'update_by': record.payment_id.write_uid.name,
                            # Bash observation
                            'bash_observation': record.payment_id.communication,

                            # ### INFORMATIONS RELATIVES AU SECOND RAPPORT ###

                            # No Facture
                            'facture_no': record.invoice_id.reference,
                            # Journal Facture
                            'journal_fact': record.invoice_id.journal_id.name,
                            # No Piece
                            'no_piece': record.invoice_id.number,
                            # Agence
                            'agence': record.invoice_id.agence_id.name,
                            # Sattut facture
                            'status_fact': record.invoice_id.state,
                            # Période
                            # 'period': periode(record.invoice_id.invoice_line_ids),
                            'period': record.invoice_id.periode_mois,
                            # Article
                            # 'article': record.invoice_id.invoice_line_ids
                            'article': articles(record.invoice_id.invoice_line_ids),
                            'compte': compte(record.invoice_id.invoice_line_ids),
                            'tag': tag(record.invoice_id.invoice_line_ids),
                            'residual': record.invoice_id.residual,
                            # Facture crée le
                            'fact_created_at': record.invoice_id.create_date.date(),
                            # Facture crée par
                            'fact_created_by': record.invoice_id.create_uid.name,
                            # comptabilisé le
                            'ct_at': record.invoice_id.date,
                            # comptabilisé par
                            'ct_by': record.invoice_id.move_id.create_uid.name,
                            'maj_at': record.invoice_id.move_id.write_date.date(),
                            'maj_by': record.invoice_id.move_id.write_uid.name,

                            # ### INFORMATIONS RELATIVES AU 3ème RAPPORT ###

                            # date facture
                            'date_fact': record.invoice_id.date_invoice,
                            # delai date_fact - brml
                            'delai_dfa_brml': delai_dfa_brml,
                            # date bon de commande
                            'date_bc': date_bc if date_bc != datetime(1, 1, 1, 0, 0).date() else None,
                            # delai date_bc - date_brml
                            'delai_bc_brml': delai_bc_brml,
                            # bon de livraison
                            'date_bl': date_bl if date_bl != datetime(1, 1, 1, 0, 0).date() else None,
                            # delai date_bl - date_brml
                            'delai_bl_brml': delai_bl_brml,
                            # date bon de reception manuel
                            'date_brml': date_brml if date_brml != datetime(1, 1, 1, 0, 0).date() else None,
                            # delai date_brml - date_brml
                            'delai_brml_brml': delai_brml_brml,
                            # date bon de reception machine
                            'date_brmc': date_brmc if date_brmc != datetime(1, 1, 1, 0, 0).date() else None,
                            # delai date_brmc - date_brml
                            'delai_brmc_brml': delai_brmc_brml,
                            # delai fact_created_at - date_fact
                            'delai_dc_df': record.invoice_id.create_date.date() - record.invoice_id.date_invoice,
                            # date à laquelle la facture est passée au statut ouvert
                            'date_validation': record.invoice_id.move_id.date,
                            # delai date_validation - fact_created_at
                            'delai_dv_dc': record.invoice_id.move_id.date - record.invoice_id.create_date.date(),
                            # delai date_brml - date_validation
                            'delaitt_brml_dv': delaitt_dv_brml,
                            # condition de paiement
                            'cond_paiment': record.invoice_id.condition_paiement,
                            # date écheance
                            'date_echeance': record.invoice_id.date_due,
                            # date de paiement
                            'date_payment': record.payment_id.payment_date,
                            # date_paiment - date_echeance
                            'echu_verif': (
                                    record.invoice_id.date - record.invoice_id.date_due) if record.invoice_id.date and record.invoice_id.date_due else None,
                        })
                        number_of_bash_selected = number_of_bash_selected + 1

        # ON RENVOIE UN DICTIONNAIRE DE LISTE VERS LE AbstractModel
        return {
            'data': result,
            'number_of_bash_selected': number_of_bash_selected,
        }

    # ## GENERATE PDF REPORT
    def print_report_pdf(self):
        data = self.get_data()
        return self.env.ref('bash_payment_report.bash_landscape_report_pdf').report_action([], data=data)

    # ## GENERATE EXCEL REPORT
    def print_report_excel(self):
        data = self.get_data()
        return self.env.ref('bash_payment_report.report_bash_payment_xls').report_action(self, data=data)

    # ## ON SAUVEGARDE LES DONNEES A IMPRIMER
    def data_to_print(self):
        # On envoie les données à la vue d'impression
        data = self.get_data()
        result = data['data']
        number_of_bash_selected = data['number_of_bash_selected']

        global_bash = self.env['global.account.bash.payment']

        # On recupère les donées à imprimer
        global_data = global_bash.search([])

        if result:
            amount = 0
            created_by = ''
            update_by = ''
            fact_created_by = ''
            facture_no = {}
            no_piece = {}
            # DELAI
            dfa_brml = {}
            bc_brml = {}
            bl_brml = {}
            brml_brml = {}
            brmc_brml = {}
            dc_df = {}
            dv_dc = {}
            brml_dv = {}

            partner2 = {}
            bash_no = {}
            journal = {}
            agence2 = {}
            statut2 = {}
            period2 = {}
            article2 = {}
            compte2 = {}
            tag2 = {}
            montant2 = {}
            cree_le = {}
            cree_par = {}
            compt_le = {}
            compt_par = {}
            maj_at = {}
            maj_par = {}

            date_fact = {}
            date_bc = {}
            date_bl = {}
            date_brml = {}
            date_brmc = {}
            date_vali = {}
            cond_pay = {}
            date_ech = {}
            date_payment = {}
            echu_ver = {}

            # facture_no = """"""
            # no_piece = """"""
            # bc_brml = """"""
            # bl_brml = """"""
            # brml_brml = """"""
            # brmc_brml = """"""

            # On calcule le montant total des factures pour un fournisseurs particulier
            # for val in result:
            #     amount += val['bash_amount']
            amount = result[0]['bash_amount']

            # On reformate le nom du createur d'enregistrement par ces initiaux
            for val in result[0]['created_by'].split():
                created_by += '.' + val[0] if created_by != '' else val[0]

            # On reformate le nom du createur d'enregistrement de la facture par ces initiaux
            for val in result[0]['fact_created_by'].split():
                fact_created_by += '.' + val[0] if fact_created_by != '' else val[0]

            def init_name(name=''):
                initial = ''
                for val in name.split():
                    initial += '.' + val[0] if initial != '' else val[0]
                return initial

            def get_product_name(data):
                product_name = ''
                for val in data:
                    product_name += ' ' + str(val['name'])
                return product_name.strip(' ')

            def format_date(date):
                year = str(date.year)
                month = str(date.month)
                day = str(date.day)
                if len(day) == 1:
                    day = '0' + day
                if len(month) == 1:
                    month = '0' + month
                result = day + '.' + month + '.' + year[2] + year[3]
                return result

            def sep(s, thou=' '):
                integer, decimal = s.split('.')
                integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
                return integer

            # N° Facture, N° Piece, delai_bc_brml, delai_bl_brml, delai_brml_brml, delai_brmc_brml
            i = 1
            for val in result:
                facture_no[i] = val['facture_no']
                no_piece[i] = val['no_piece']
                dfa_brml[i] = val['delai_dfa_brml'].days if val['delai_dfa_brml'] != None else ''
                bc_brml[i] = val['delai_bc_brml'].days if val['delai_bc_brml'] != None else ''
                bl_brml[i] = val['delai_bl_brml'].days if val['delai_bl_brml'] != None else ''
                brml_brml[i] = val['delai_brml_brml'].days if val['delai_brml_brml'] != None else ''
                brmc_brml[i] = val['delai_brmc_brml'].days if val['delai_brmc_brml'] != None else ''
                dc_df[i] = val['delai_dc_df'].days if val['delai_dc_df'] != None else ''
                dv_dc[i] = val['delai_dv_dc'].days if val['delai_dv_dc'] != None else ''
                brml_dv[i] = val['delaitt_brml_dv'].days if val['delaitt_brml_dv'] != None else ''

                partner2[i] = val['partner'] if val['partner'] else ''
                bash_no[i] = val['bash_no'] if val['bash_no'] else ''
                journal[i] = val['journal_fact'] if val['journal_fact'] else ''
                agence2[i] = val['agence'] if val['agence'] else ''
                statut2[i] = val['status_fact'] if val['status_fact'] else ''
                period2[i] = val['period'] if val['period'] else ''
                article2[i] = get_product_name(val['article']) if val['article'] else ''
                compte2[i] = get_product_name(val['compte']) if val['compte'] else ''
                tag2[i] = get_product_name(val['tag']) if val['tag'] else ''
                montant2[i] = sep("%.2f" % val['residual']) if val['residual'] else ''
                cree_le[i] = format_date(val['fact_created_at']) if val['fact_created_at'] else ''
                cree_par[i] = init_name(val['fact_created_by']) if val['fact_created_by'] else ''
                compt_le[i] = format_date(val['ct_at']) if val['ct_at'] else ''
                compt_par[i] = init_name(val['ct_by']) if val['ct_by'] else ''
                maj_at[i] = format_date(val['maj_at']) if val['maj_at'] else ''
                maj_par[i] = init_name(val['maj_by']) if val['maj_by'] else ''

                date_fact[i] = format_date(val['date_fact']) if val['date_fact'] else ''
                date_bc[i] = format_date(val['date_bc']) if val['date_bc'] else ''
                date_bl[i] = format_date(val['date_bl']) if val['date_bl'] else ''
                date_brml[i] = format_date(val['date_brml']) if val['date_brml'] else ''
                date_brmc[i] = format_date(val['date_brmc']) if val['date_brmc'] else ''
                date_vali[i] = format_date(val['date_validation']) if val['date_validation'] else ''
                cond_pay[i] = val['cond_paiment'] if val['cond_paiment'] else ''
                date_ech[i] = format_date(val['date_echeance']) if val['date_echeance'] else ''
                date_payment[i] = format_date(val['date_payment']) if val['date_payment'] else ''
                echu_ver[i] = val['echu_verif'].days if val['echu_verif'] != None else ''

                # facture_no += ("\n" + str(i) + ": " + str(val['facture_no'])) if facture_no else ("\n" + str(i) + ": " + str(val['facture_no']))
                # no_piece += ("\n" + str(i) + ": " + str(val['no_piece'])) if no_piece else ("\n" + str(i) + ": " + str(val['no_piece']))
                # bc_brml += (("\n" + str(i) + ": " + str(val['delai_bc_brml'].days)) if bc_brml else ("\n" + str(i) + ": " + str(val['delai_bc_brml'].days))) if val['delai_bc_brml'] else (("\n" + str(i) + ": --") if bc_brml else ("\n" + str(i) + ": --"))
                # bl_brml += (("\n" + str(i) + ": " + str(val['delai_bl_brml'].days)) if bl_brml else ("\n" + str(i) + ": " + str(val['delai_bl_brml'].days))) if val['delai_bl_brml'] else (("\n" + str(i) + ": --") if bl_brml else ("\n" + str(i) + ": --"))
                # brml_brml += (("\n" + str(i) + ": " + str(val['delai_brml_brml'].days)) if brml_brml else ("\n" + str(i) + ": " + str(val['delai_brml_brml'].days))) if val['delai_brml_brml'] else (("\n" + str(i) + ": --") if brml_brml else ("\n" + str(i) + ": --"))
                # brmc_brml += (("\n" + str(i) + ": " + str(val['delai_brmc_brml'].days)) if brmc_brml else ("\n" + str(i) + ": " + str(val['delai_brmc_brml'].days))) if val['delai_brmc_brml'] else (("\n" + str(i) + ": --") if brmc_brml else ("\n" + str(i) + ": --"))
                i += 1

            # On reformate le nom de l'utilisateur qui a mis à jour l'enregistrement par ces initiaux
            for val in result[0]['update_by'].split():
                update_by += '.' + val[0] if update_by != '' else val[0]

            exist = False
            period = ''
            article = ''
            compte = ''
            tag = ''
            # for val in result[0]['period']:
            #     period += ' ' + str(val['name'])
            for val in result[0]['article']:
                article += ' ' + str(val['name'])
            for val in result[0]['compte']:
                compte += ' ' + str(val['name'])
            for val in result[0]['tag']:
                tag += ' ' + str(val['name'])

            data_store = {
                # Bash 1
                'fournisseur_print': result[0]['partner'],
                'bash_no_print': result[0]['bash_no'],
                'reglement_print': result[0]['rule'],
                'no_cheque_print': result[0]['no_cheque'],
                'journal_print': result[0]['journal'],
                'bash_date_print': result[0]['bash_date'],
                'bash_status_print': result[0]['bash_status'],
                'bash_nbr_print': number_of_bash_selected,
                'bash_amount_print': amount,
                'created_at_print': result[0]['created_at'],
                'created_by_print': created_by,
                'update_at_print': result[0]['updated_at'],
                'update_by_print': update_by,
                'bash_observation_print': result[0]['bash_observation'],

                # Bash 2
                'fournisseur_bash2': str(partner2),
                'no_bash2': str(bash_no),
                'facture_no_print': str(facture_no),
                'journal_fact_print': str(journal),
                'no_piece_print': str(no_piece),
                'agence_print': str(agence2),
                'status_fact_print': str(statut2),
                'period_print': str(period2),
                'article_print': str(article2),
                'compte_print': str(compte2),
                'tag_print': str(tag2),
                'residual_print': str(montant2),
                'fact_created_at_print': str(cree_le),
                'fact_created_by_print': str(cree_par),
                'ct_at_print': str(compt_le),
                'ct_by_print': str(compt_par),
                'maj_at_print': str(maj_at),
                'maj_par_print': str(maj_par),

                # Bash 3
                'date_fact_print': str(date_fact),
                'delai_dfa_brml_print': str(dfa_brml),
                'date_bc_print': str(date_bc),
                'delai_bc_brml_print': str(bc_brml),
                'date_bl_print': str(date_bl),
                'delai_bl_brml_print': str(bl_brml),
                'date_brml_print': str(date_brml),
                'delai_brml_brml_print': str(brml_brml),
                'date_brmc_print': str(date_brmc),
                'delai_brmc_brml_print': str(brmc_brml),
                'delai_dc_df_print': str(dc_df),
                'date_validation_print': str(date_vali),
                'delai_dv_dc_print': str(dv_dc),
                'delaitt_brml_dv_print': str(brml_dv),
                'cond_paiment_print': str(cond_pay),
                'date_echeance_print': str(date_ech),
                'date_payment_print': str(date_payment),
                'echu_verif_print': str(echu_ver),
            }
            if global_data:
                # On parcourt les données à imprimer
                for record in global_data:
                    if result[0]['bash_no'] == record.bash_no_print:
                        record.write(data_store)
                        exist = True

            if not exist:
                # # On enregistre les données
                global_bash.create(data_store)


class GlobalReportBashPayment(models.Model):
    _name = 'global.account.bash.payment'

    imprimee = fields.Boolean(default=False, store=True)
    non_imprimee = fields.Boolean(default=True, store=True)

    # DONNEES RELATIVES AU BASH 1
    fournisseur_print = fields.Char(string="Fournisseur", store=True)
    bash_no_print = fields.Char(string="Bash no", store=True)
    reglement_print = fields.Char(string="Reg", store=True)
    no_cheque_print = fields.Char(string="No cheque", store=True)
    journal_print = fields.Char(string="Journal", store=True)
    bash_date_print = fields.Date(string="Bash date", store=True)
    bash_status_print = fields.Char(string="Bash status", store=True)
    bash_nbr_print = fields.Char(string="Bash nbr", store=True)
    bash_amount_print = fields.Float(string="Montant", store=True)
    created_at_print = fields.Date(string="Date création", store=True)
    created_by_print = fields.Char(string="Créer par", store=True)
    update_at_print = fields.Date(string="Date MAJ", store=True)
    update_by_print = fields.Char(string="Créer par", store=True)
    bash_observation_print = fields.Char(string="Observation", store=True)

    # DONNEES RELATIVES AU BASH 2
    fournisseur_bash2 = fields.Char(string="Fournisseur bash 2", store=True)
    no_bash2 = fields.Char(string="N° Bash2", store=True)
    facture_no_print = fields.Char(string="No Facture", store=True)
    journal_fact_print = fields.Char(store=True)
    no_piece_print = fields.Char(string="No Piece", store=True)
    agence_print = fields.Char(string="Ag", store=True)
    status_fact_print = fields.Char(store=True)
    period_print = fields.Char(string="Periode", store=True)
    article_print = fields.Char(string="Article", store=True)
    compte_print = fields.Char(string="Compte", store=True)
    tag_print = fields.Char(string="Tag", store=True)
    # residual_print = fields.Float(store=True)
    residual_print = fields.Char(store=True)
    # fact_created_at_print = fields.Date(store=True)
    fact_created_at_print = fields.Char(store=True)
    fact_created_by_print = fields.Char(store=True)
    # ct_at_print = fields.Date(string="CT le", store=True)
    ct_at_print = fields.Char(string="CT le", store=True)
    ct_by_print = fields.Char(string="CT par", store=True)
    maj_at_print = fields.Char(string="MAJ le", store=True)
    maj_par_print = fields.Char(string="MAJ par", store=True)

    # DONNEES RELATIVES AU BASH 3
    # date_fact_print = fields.Date(string="Date facture", store=True)
    date_fact_print = fields.Char(string="Date facture", store=True)
    delai_dfa_brml_print = fields.Char(string='Delai Dfa-BRML', store=True)
    # date_bc_print = fields.Date(string="Date BC", store=True)
    date_bc_print = fields.Char(string="Date BC", store=True)
    delai_bc_brml_print = fields.Char(string="Delai BC-BRML", store=True)
    # date_bl_print = fields.Date(string="Date BL", store=True)
    date_bl_print = fields.Char(string="Date BL", store=True)
    delai_bl_brml_print = fields.Char(string="Delai BL-BRML", store=True)
    # date_brml_print = fields.Date(string="DATE BRML", store=True)
    date_brml_print = fields.Char(string="DATE BRML", store=True)
    delai_brml_brml_print = fields.Char("Delai BRML-BRML", store=True)
    date_brmc_print = fields.Char(string="Date BRMC", store=True)
    delai_brmc_brml_print = fields.Char(string="Delai BRMC-BRML", store=True)
    delai_dc_df_print = fields.Char(string="Delai Date creation - Date facture", store=True)
    # date_validation_print = fields.Date(string="Date Validation", store=True)
    date_validation_print = fields.Char(string="Date Validation", store=True)
    delai_dv_dc_print = fields.Char(string="Delai Date validation - Date creation", store=True)
    delaitt_brml_dv_print = fields.Char(string="Date BRML - Date creation", store=True)
    cond_paiment_print = fields.Char(string="Cond. paiement", store=True)
    # date_echeance_print = fields.Date(string="Date echeance", store=True)
    date_echeance_print = fields.Char(string="Date echeance", store=True)
    date_payment_print = fields.Char(string="DP", store=True)
    echu_verif_print = fields.Char(string="Echu verif", store=True)

    def format_data(self):
        bash = {
            'founisseur': ast.literal_eval(self.fournisseur_bash2),
            'no_bash': ast.literal_eval(self.no_bash2),
            'no_fact': ast.literal_eval(self.facture_no_print),
            'journal': ast.literal_eval(self.journal_fact_print),
            'no_piece': ast.literal_eval(self.no_piece_print),
            'agence': ast.literal_eval(self.agence_print),
            'status': ast.literal_eval(self.status_fact_print),
            'period': ast.literal_eval(self.period_print),
            'article': ast.literal_eval(self.article_print),
            'compte': ast.literal_eval(self.compte_print),
            'tag': ast.literal_eval(self.tag_print),
            'residual': ast.literal_eval(self.residual_print),
            'created_at': ast.literal_eval(self.fact_created_at_print),
            'created_by': ast.literal_eval(self.fact_created_by_print),
            'ct_at': ast.literal_eval(self.ct_at_print),
            'ct_by': ast.literal_eval(self.ct_by_print),
            'maj_at': ast.literal_eval(self.maj_at_print),
            'maj_by': ast.literal_eval(self.maj_par_print),

            'date_fact': ast.literal_eval(self.date_fact_print),
            'delai_dfa_brml': ast.literal_eval(self.delai_dfa_brml_print),
            'date_bc': ast.literal_eval(self.date_bc_print),
            'delai_bc_brml': ast.literal_eval(self.delai_bc_brml_print),
            'date_bl': ast.literal_eval(self.date_bl_print),
            'delai_bl_brml': ast.literal_eval(self.delai_bl_brml_print),
            'date_brml': ast.literal_eval(self.date_brml_print),
            'delai_brml_brml': ast.literal_eval(self.delai_brml_brml_print),
            'date_brmc': ast.literal_eval(self.date_brmc_print),
            'delai_brmc_brml': ast.literal_eval(self.delai_brmc_brml_print),
            'delai_dc_df': ast.literal_eval(self.delai_dc_df_print),
            'date_validation': ast.literal_eval(self.date_validation_print),
            'delai_dv_dc': ast.literal_eval(self.delai_dv_dc_print),
            'delaitt_brml_dv': ast.literal_eval(self.delaitt_brml_dv_print),
            'cond_paiment': ast.literal_eval(self.cond_paiment_print),
            'date_echeance': ast.literal_eval(self.date_echeance_print),
            'date_payment': ast.literal_eval(self.date_payment_print),
            'echu_verif': ast.literal_eval(self.echu_verif_print),
        }
        return bash

    # FONCTION QUI SAUVEGARDE LES ID DES BASH IMPTRIMES
    @api.model
    def get_active_ids(self, val_list):
        # val_list EST LE DICT DES ID A SAUVEGARDER PROVENANT DE L'OBJET JAVASCRIPT
        for elt in val_list:
            self.env['global.account.bash.payment'].search([('id', '=', elt)]).write({'imprimee': True, 'non_imprimee': False})


class ExtendCancelBash(models.Model):
    _inherit = 'account.bash.payment'

    @api.multi
    def cancel(self):
        super(ExtendCancelBash, self).cancel()
        manager = self.env['global.account.bash.payment']
        bash = self.env['account.bash.payment'].search([('id', '=', self.id)])
        cancel_saved_bash = manager.search([('bash_no_print', '=', bash.name)])  # ON RECUPERE SON EQUIVALENT
        if cancel_saved_bash:
            cancel_saved_bash.unlink()  # ON CANCEL LA CORRESPONDANCE DU BASH
