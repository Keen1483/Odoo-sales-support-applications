# -*- coding: utf-8 -*-

from odoo import models, fields, api

import re


class RapportBpJournalier(models.Model):
    _inherit = 'caisse_depense_rapport.bpjournalier'

    def pdf_xls_data(self):
        fas = self.facture_ids
        rts = self.reste_ids
        gds = self.garder_ids
        nb_lines = max(len(fas), len(rts), len(gds))
        data_lines = {}

        if nb_lines == 0:
            data_lines[1] = {
                # BP
                'bp_no': self.name,
                'bp_date': self.Date_jour,
                'pb_description': self.describe,
                'bp_amount': self.amount,
                'bp_status': self.state,
                # FACTURES
                'fa_no': '',
                'fa_date': '',
                'fa_amount': '',
                # RESTES
                'rt_no': '',
                'rt_date': '',
                'rt_amount': '',
                # GARDES
                'gd_date': '',
                'gd_k_amount': '',
                'gd_r_amount': ''
            }
        else:
            # FACTURES
            fas_dict = {}
            if fas:
                i = 1
                for record in fas:
                    fas_dict[i] = {
                        'no': record.numero,
                        'date': record.date_fac,
                        'amount': record.montant,
                    }
                    i += 1
            if len(fas_dict) != nb_lines:
                i = len(fas_dict) + 1
                while len(fas_dict) < nb_lines:
                    fas_dict[i] = {
                        'no': '',
                        'date': '',
                        'amount': '',
                    }
                    i += 1

            # RESTES
            rts_dict = {}
            if rts:
                j = 1
                for record in rts:
                    rts_dict[j] = {
                        'no': record.numero,
                        'date': record.create_date.date(),
                        'amount': record.montant,
                    }
                    j += 1
            if len(rts_dict) != nb_lines:
                j = len(rts_dict) + 1
                while len(rts_dict) < nb_lines:
                    rts_dict[j] = {
                        'no': '',
                        'date': '',
                        'amount': '',
                    }
                    j += 1

            # GARDES
            gds_dict = {}
            if gds:
                k = 1
                for record in gds:
                    gds_dict[k] = {
                        'date': record.date_g,
                        'k_amount': record.amount_garder,
                        'r_amount': record.amount_retirer,
                    }
                    k += 1
            if len(gds_dict) != nb_lines:
                k = len(gds_dict) + 1
                while len(gds_dict) < nb_lines:
                    gds_dict[k] = {
                        'date': '',
                        'k_amount': '',
                        'r_amount': '',
                    }
                    k += 1

        # DICTIONNAIRE RENDU
        for l in range(1, nb_lines + 1):
            data_lines[l] = {
                # BP
                'bp_no': self.name,
                'bp_date': self.Date_jour,
                'pb_description': self.describe,
                'bp_amount': self.amount,
                'bp_status': self.state,
                # FACTURES
                'fa_no': fas_dict[l]['no'],
                'fa_date': fas_dict[l]['date'],
                'fa_amount': fas_dict[l]['amount'],
                # RESTES
                'rt_no': rts_dict[l]['no'],
                'rt_date': rts_dict[l]['date'],
                'rt_amount': rts_dict[l]['amount'],
                # GARDES
                'gd_date': gds_dict[l]['date'],
                'gd_k_amount': gds_dict[l]['k_amount'],
                'gd_r_amount': gds_dict[l]['r_amount']
            }
        return data_lines

    def pdf_data(self):
        def sep(s, thou=' '):
            integer, decimal = s.split('.')
            integer = re.sub(r"\B(?=(?:\d{3})+$)", thou, integer)
            return integer

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

        data = self.pdf_xls_data()
        for record in data:
            data[record]['bp_date'] = format_date(data[record]['bp_date']) if not isinstance(data[record]['bp_date'], str) else ''
            data[record]['bp_amount'] = sep("%.2f" % data[record]['bp_amount']) if not isinstance(data[record]['bp_amount'], str) else ''
            data[record]['fa_date'] = format_date(data[record]['fa_date']) if not isinstance(data[record]['fa_date'], str) else ''
            data[record]['fa_amount'] = sep("%.2f" % data[record]['fa_amount']) if not isinstance(data[record]['fa_amount'], str) else ''
            data[record]['rt_date'] = format_date(data[record]['rt_date']) if not isinstance(data[record]['rt_date'], str) else ''
            data[record]['rt_amount'] = sep("%.2f" % data[record]['rt_amount']) if not isinstance(data[record]['rt_amount'], str) else ''
            data[record]['gd_date'] = format_date(data[record]['gd_date']) if not isinstance(data[record]['gd_date'], str) else ''
            data[record]['gd_k_amount'] = sep("%.2f" % data[record]['gd_k_amount']) if not isinstance(data[record]['gd_k_amount'], str) else ''
            data[record]['gd_r_amount'] = sep("%.2f" % data[record]['gd_r_amount']) if not isinstance(data[record]['gd_r_amount'], str) else ''
        return data

    def sum_amount(self):
        sums = {
            'sum_bp': 0,
            'sum_fa': 0,
            'sum_rt': 0,
            'sum_kk': 0,
            'sum_kr': 0,
        }
        data = self.pdf_xls_data()
        for record in data:
            sums['sum_bp'] += 0 if isinstance([record]['bp_amount'], str) else [record]['bp_amount']
            sums['sum_fa'] += 0 if isinstance([record]['fa_amount'], str) else [record]['fa_amount']
            sums['sum_rt'] += 0 if isinstance([record]['rt_amount'], str) else [record]['rt_amount']
            sums['sum_kk'] += 0 if isinstance([record]['gd_k_amount'], str) else [record]['gd_k_amount']
            sums['sum_kr'] += 0 if isinstance([record]['gd_r_amount'], str) else [record]['gd_r_amount']
        return sums

