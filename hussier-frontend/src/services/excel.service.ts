import { Injectable } from '@angular/core';
import * as XLSX from 'xlsx';

@Injectable({
  providedIn: 'root'
})
export class ExcelService {

  exportToExcel(data: any[], fileName: string, sheetName: string = 'Donnees'): void {
    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);

    const colWidths = Object.keys(data[0] || {}).map(key => {
      const maxLen = Math.max(
        key.length,
        ...data.map(row => String(row[key] ?? '').length)
      );
      return { wch: Math.min(maxLen + 2, 40) };
    });
    worksheet['!cols'] = colWidths;

    XLSX.writeFile(workbook, `${fileName}.xlsx`);
  }

  exportDossiers(dossiers: any[]): void {
    const data = dossiers.map(d => ({
      'Numéro': d.numero_dossier || '',
      'Objet': d.objet || '',
      'Type': d.type_dossier || '',
      'Statut': d.statut || '',
      'Date ouverture': d.date_ouverture ? new Date(d.date_ouverture).toLocaleDateString('fr-FR') : ''
    }));
    this.exportToExcel(data, 'dossiers', 'Dossiers');
  }

  exportClients(clients: any[]): void {
    const data = clients.map(c => ({
      'Nom': c.nom || '',
      'Prénom': c.prenom || '',
      'Type': c.type_client || '',
      'Téléphone': c.telephone || '',
      'Email': c.email || '',
      'Adresse': c.adresse || ''
    }));
    this.exportToExcel(data, 'clients', 'Clients');
  }

  exportPaiements(paiements: any[]): void {
    const data = paiements.map(p => ({
      'Date': p.date_paiement ? new Date(p.date_paiement).toLocaleDateString('fr-FR') : '',
      'Type': p.type_paiement || '',
      'Libellé': p.libelle || '',
      'Mode': p.mode_paiement || '',
      'Montant (FCFA)': p.montant || 0
    }));
    this.exportToExcel(data, 'paiements', 'Paiements');
  }

  exportActes(actes: any[]): void {
    const data = actes.map(a => ({
      'Type': a.type_acte || '',
      'Date': a.date_acte ? new Date(a.date_acte).toLocaleDateString('fr-FR') : '',
      'Lieu': a.lieu || '',
      'Résultat': a.resultat || ''
    }));
    this.exportToExcel(data, 'actes', 'Actes');
  }
}
