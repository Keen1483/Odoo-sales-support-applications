import base64
import io
from odoo import models
from datetime import datetime, date


# ## CLASSE DU RAPPORT PAR UN BOUTON CUSTOMISE
# class PaymentXLS(models.AbstractModel):
#     _name = 'report.bash_payment_report.report_bash_payment_id_xls'
#     _inherit = 'report.report_xlsx.abstract'
#
#     # data contient toutes le doonées du model
#     # bash contient le record courant
#
#     def generate_xlsx_report(self, workbook, data, bash):
#         bold = workbook.add_format({'bold': True})
#         regular = workbook.add_format({'bold': False})
#         format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'blue', 'color': '#FFFFFF'})
#
#         # On recupère la variable data envoyé depuis le model
#         data_list = data['data']
#         sheet = workbook.add_worksheet('Bash 1')
#         row = 1
#         col = 1
#
#         # On definie la largeur des colonne
#         # sheet.set_column('E:E', 13)
#         sheet.set_column(1, 14, 15)
#
#         # Titre de la feuille excel
#         # row += 1
#         # sheet.merge_range(row, col, row, col + 13, 'Bash de Paiement', format_1)
#
#         # On definie l'enête de tableau excel
#         row += 1
#         col_tile = col
#         thead = ['Fournisseur', 'Bash no', 'Reglement', 'No Cheque', 'Journal', 'Bash date', 'Bash statut', 'Bash nbr facture', 'Bash montant', 'Bash crée le', 'Bash crée par', 'Bash Date MAJ', 'Bash MAJ par', 'Bash observation']
#         for th in thead:
#             sheet.write(row, col_tile, th, bold)
#             col_tile += 1
#
#         # On écrit ligne par ligne
#         for obj in data_list:
#             row += 1
#             col_row = col
#
#             # On écrit cellule par cellule sur la même ligne
#             for elt in obj:
#                 sheet.write(row, col_row, obj[elt], regular)
#                 col_row += 1


# ## CLASSE DU RAPPORT PAR LE BOUTON NATIF IMPRIMER
class globalBash(models.AbstractModel):
    _name = 'report.bash_payment_report.report_bash_payment_btn_print_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, bash_record):
        bold = workbook.add_format({'bold': True})
        regular = workbook.add_format({'bold': False, 'num_format': 'dd/mm/yyyy'})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'blue', 'color': '#FFFFFF'})

        def reform_date(date_str):
            date_str = date_str.strip()
            if date_str:
                yy = date_str[-2] + date_str[-1]
                date_str = date_str[:-2] + '20' + yy
                date_normal = datetime.strptime(date_str, '%d.%m.%Y').date()
                return date_normal
            else:
                return None

        # On crée la feuille 1
        sheet = workbook.add_worksheet('Bash 1')
        row = 0
        col = 0

        # On definie la largeur des colonne
        # sheet.set_column('E:E', 13)
        sheet.set_column(0, 13, 15)

        # On definie l'enête de tableau excel
        col_tile = col
        thead = ['Fournisseur', 'Bash no', 'Reglement', 'No Cheque', 'Journal', 'Bash date', 'Bash statut', 'Bash nbr facture', 'Bash montant', 'Bash crée le', 'Bash crée par', 'Bash Date MAJ', 'Bash MAJ par', 'Bash observation']
        for th in thead:
            sheet.write(row, col_tile, th, bold)
            col_tile += 1

        # On écrit ligne par ligne
        for obj in bash_record:
            row += 1
            col_row = col
            sheet.write(row, col_row, obj.fournisseur_print)

            col_row += 1
            sheet.write(row, col_row, obj.bash_no_print)

            col_row += 1
            sheet.write(row, col_row, obj.reglement_print)

            col_row += 1
            sheet.write(row, col_row, obj.no_cheque_print)

            col_row += 1
            sheet.write(row, col_row, obj.journal_print)

            col_row += 1
            sheet.write(row, col_row, obj.bash_date_print, regular)

            col_row += 1
            sheet.write(row, col_row, obj.bash_status_print)

            col_row += 1
            sheet.write(row, col_row, obj.bash_nbr_print)

            col_row += 1
            sheet.write(row, col_row, obj.bash_amount_print)

            col_row += 1
            sheet.write(row, col_row, obj.created_at_print, regular)

            col_row += 1
            sheet.write(row, col_row, obj.created_by_print)

            col_row += 1
            sheet.write(row, col_row, obj.update_at_print)

            col_row += 1
            sheet.write(row, col_row, obj.update_by_print)

            col_row += 1
            sheet.write(row, col_row, obj.bash_observation_print)

            # On écrit cellule par cellule sur la même ligne
            # for elt in obj:
            #     sheet.write(row, col_row, obj[elt], regular)
            #     col_row += 1

        # On crée la feuille 2
        sheet_2 = workbook.add_worksheet('Bash 2')

        # On definie la largeur des colonne
        sheet_2.set_column(0, 17, 15)
        row = 0
        col = 0

        # On definie l'enête de tableau excel
        col_tile_2 = col
        thead_2 = ['Fournisseur', 'Bash No', 'No Facture', 'Journal', 'No Piece', 'Agence', 'Statut',
                 'Periode', 'Article', 'Compte', 'Tag', 'Montant', 'Crée le', 'Crée par', 'Comptabilisé le', 'Comptabilisé par', 'Mis à jour le', 'Mis à jour par']
        for th in thead_2:
            sheet_2.write(row, col_tile_2, th, bold)
            col_tile_2 += 1

        # # On écrit ligne par ligne
        for obj in bash_record:
            bash = obj.format_data()
            row_col = row
            col_row = col
            for record in bash['founisseur']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['founisseur'][record])

            col_row += 1
            row_col = row
            for record in bash['no_bash']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['no_bash'][record])

            col_row += 1
            row_col = row
            for record in bash['no_fact']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['no_fact'][record])

            col_row += 1
            row_col = row
            for record in bash['journal']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['journal'][record])

            col_row += 1
            row_col = row
            for record in bash['no_piece']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['no_piece'][record])

            col_row += 1
            row_col = row
            for record in bash['agence']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['agence'][record])

            col_row += 1
            row_col = row
            for record in bash['status']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['status'][record])

            col_row += 1
            row_col = row
            for record in bash['period']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['period'][record])

            col_row += 1
            row_col = row
            for record in bash['article']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['article'][record])

            col_row += 1
            row_col = row
            for record in bash['compte']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['compte'][record])

            col_row += 1
            row_col = row
            for record in bash['tag']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['tag'][record])

            col_row += 1
            row_col = row
            for record in bash['residual']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['residual'][record])

            col_row += 1
            row_col = row
            for record in bash['created_at']:
                row_col += 1
                sheet_2.write(row_col, col_row, reform_date(bash['created_at'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['created_by']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['created_by'][record])

            col_row += 1
            row_col = row
            for record in bash['ct_at']:
                row_col += 1
                sheet_2.write(row_col, col_row, reform_date(bash['ct_at'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['ct_by']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['ct_by'][record])

            col_row += 1
            row_col = row
            for record in bash['maj_at']:
                row_col += 1
                sheet_2.write(row_col, col_row, reform_date(bash['maj_at'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['maj_by']:
                row_col += 1
                sheet_2.write(row_col, col_row, bash['maj_by'][record])

            row = row + len(bash['ct_by'])



        # On crée la feuille 3
        sheet_3 = workbook.add_worksheet('Bash 3')

        # On definie la largeur des colonne
        sheet_3.set_column(0, 21, 15)
        row = 0
        col = 0

        # On definie l'enête descriptif
        col_t = col
        thead_3 = ['Fournisseur', 'Bash No', 'No Facture', 'DATE BRML', 'BRML-BRML', 'Date Fa', 'Delai Dfa-BRML', 'Date BC', 'BC-BRML', 'Date BL', 'BL-BRML', 'Date BRMC',
                   'BRMC-BRML', 'Crée le', 'Delai Dc-Df', 'Date Validation', 'Delai Dv-Dc', 'Delai TT DV-BR',
                   'Condition de paiement', 'Date Echéance', 'Date Paiement', 'Echu Vérif']
        for th in thead_3:
            sheet_3.write(row, col_t, th, bold)
            col_t += 1

        # On definie l'enête de tableau excel
        col_tile_3 = col
        row += 1
        thead_3 = ['Fournisseur', 'Bash No', 'No Facture', 'DBR', 'BR', 'DFA', 'FA', 'DBC', 'BC', 'DBL', 'BL', 'DSA', 'SA', 'Crée le', 'Delai Dc-Df', 'Date Validation', 'Delai Dv-Dc', 'Delai TT DV-BR', 'Condition de paiement', 'Date Echéance', 'Date Paiement', 'Echu Vérif']
        for th in thead_3:
            sheet_3.write(row, col_tile_3, th, bold)
            col_tile_3 += 1

        # # On écrit ligne par ligne
        for obj in bash_record:
            bash = obj.format_data()
            row_col = row
            col_row = col
            for record in bash['founisseur']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['founisseur'][record])

            col_row += 1
            row_col = row
            for record in bash['no_bash']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['no_bash'][record])

            col_row += 1
            row_col = row
            for record in bash['no_fact']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['no_fact'][record])

            col_row += 1
            row_col = row
            for record in bash['date_brml']:
                row_col += 1
                sheet_3.write(row_col, col_row, reform_date(bash['date_brml'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['delai_brml_brml']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['delai_brml_brml'][record])

            col_row += 1
            row_col = row
            for record in bash['date_fact']:
                row_col += 1
                sheet_3.write(row_col, col_row, reform_date(bash['date_fact'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['delai_dfa_brml']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['delai_dfa_brml'][record])

            col_row += 1
            row_col = row
            for record in bash['date_bc']:
                row_col += 1
                sheet_3.write(row_col, col_row, reform_date(bash['date_bc'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['delai_bc_brml']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['delai_bc_brml'][record])

            col_row += 1
            row_col = row
            for record in bash['date_bl']:
                row_col += 1
                sheet_3.write(row_col, col_row, reform_date(bash['date_bl'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['delai_bl_brml']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['delai_bl_brml'][record])

            col_row += 1
            row_col = row
            for record in bash['date_brmc']:
                row_col += 1
                sheet_3.write(row_col, col_row, reform_date(bash['date_brmc'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['delai_brmc_brml']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['delai_brmc_brml'][record])

            col_row += 1
            row_col = row
            for record in bash['created_at']:
                row_col += 1
                sheet_3.write(row_col, col_row, reform_date(bash['created_at'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['delai_dc_df']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['delai_dc_df'][record])

            col_row += 1
            row_col = row
            for record in bash['date_validation']:
                row_col += 1
                sheet_3.write(row_col, col_row, reform_date(bash['date_validation'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['delai_dv_dc']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['delai_dv_dc'][record])

            col_row += 1
            row_col = row
            for record in bash['delaitt_brml_dv']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['delaitt_brml_dv'][record])

            col_row += 1
            row_col = row
            for record in bash['cond_paiment']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['cond_paiment'][record])

            col_row += 1
            row_col = row
            for record in bash['date_echeance']:
                row_col += 1
                sheet_3.write(row_col, col_row, reform_date(bash['date_echeance'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['date_payment']:
                row_col += 1
                sheet_3.write(row_col, col_row, reform_date(bash['date_payment'][record]), regular)

            col_row += 1
            row_col = row
            for record in bash['echu_verif']:
                row_col += 1
                sheet_3.write(row_col, col_row, bash['echu_verif'][record])

            row = row + len(bash['echu_verif'])
