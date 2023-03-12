# -*- coding: utf-8 -*-

from odoo import models


class ReportXlsx(models.AbstractModel):
    _name = 'report.rapport_pb_journalier.rapport_bp_journalier_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, document):
        bold = workbook.add_format({'bold': True})
        border = workbook.add_format({'border': 1})
        bold_center = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'border': 1})

        # CREATION DE LA FEUILLE
        sheet = workbook.add_worksheet('Rapport BP')

        sheet.merge_range(0, 0, 0, 4, 'Bons Provisoires', bold_center)
        sheet.merge_range(0, 5, 0, 7, 'Factures', bold_center)
        sheet.merge_range(0, 8, 0, 10, 'Retour BP', bold_center)
        sheet.merge_range(0, 11, 0, 13, 'Gardés', bold_center)

        row = 1
        col = 0

        # LARGEUR DE LA COLONNE
        sheet.set_column(0, 13, 15)

        # ENTETE DU TABLEAU
        col_title = col
        thead = ['N°', 'Date', 'Description', 'Montant', 'Statut', 'N°', 'Date', 'Montant', 'N°', 'Date', 'Montant', 'Date', 'Montant gardé', 'Montant retiré']

        for th in thead:
            sheet.write(row, col_title, th, bold_center)
            col_title += 1

        for records in document:
            record = records.pdf_xls_data()
            for line in record:
                row += 1
                col_row = col
                for cell in record[line]:
                    if cell in ['bp_date', 'fa_date', 'rt_date', 'gd_date']:
                        sheet.write(row, col_row, record[line][cell], date_format)
                    else:
                        sheet.write(row, col_row, record[line][cell], border)
                    col_row += 1
