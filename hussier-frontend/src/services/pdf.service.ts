import { Injectable } from '@angular/core';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

@Injectable({
  providedIn: 'root'
})
export class PdfService {

  private addHeader(doc: jsPDF, titre: string) {
    doc.setFillColor(30, 58, 95);
    doc.rect(0, 0, 210, 25, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.text('Cabinet Me SAWADOGO', 14, 12);
    doc.setFontSize(10);
    doc.text('Huissier de Justice - Ouagadougou', 14, 19);
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(14);
    doc.setFont('helvetica', 'bold');
    doc.text(titre, 14, 35);
    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(100, 100, 100);
    doc.text('Genere le : ' + new Date().toLocaleDateString('fr-FR'), 14, 42);
    doc.setTextColor(0, 0, 0);
  }

  exportDossiers(dossiers: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Dossiers');
    autoTable(doc, {
      startY: 48,
      head: [['Numero', 'Objet', 'Type', 'Statut', 'Date ouverture']],
      body: dossiers.map(d => [
        d.numero_dossier || '',
        d.objet || '',
        d.type_dossier || '',
        d.statut || '',
        d.date_ouverture ? new Date(d.date_ouverture).toLocaleDateString('fr-FR') : ''
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('dossiers.pdf');
  }

  exportClients(clients: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Clients');
    autoTable(doc, {
      startY: 48,
      head: [['Nom', 'Prenom', 'Type', 'Telephone', 'Email', 'Adresse']],
      body: clients.map(c => [
        c.nom || '',
        c.prenom || '',
        c.type_client || '',
        c.telephone || '',
        c.email || '',
        c.adresse || ''
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('clients.pdf');
  }

  exportFicheClient(client: any, dossiers: any[], paiements: any[]) {
    const doc = new jsPDF();
    doc.setFillColor(30, 58, 95);
    doc.rect(0, 0, 210, 35, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(18);
    doc.setFont('helvetica', 'bold');
    doc.text('FICHE CLIENT', 14, 15);
    doc.setFontSize(11);
    doc.text('Cabinet Me SAWADOGO - Huissier de Justice', 14, 23);
    doc.setFontSize(9);
    doc.text('Genere le : ' + new Date().toLocaleDateString('fr-FR'), 14, 30);
    doc.setTextColor(0, 0, 0);
    const nomComplet = client.prenom ? client.nom + ' ' + client.prenom : client.nom;
    autoTable(doc, {
      startY: 42,
      body: [
        ['Nom complet', nomComplet],
        ['Type', client.type_client || ''],
        ['Telephone', client.telephone || ''],
        ['Email', client.email || ''],
        ['Adresse', client.adresse || ''],
        ['SIRET/NIF', client.siret || ''],
        ['Representant legal', client.representant_legal || ''],
      ],
      styles: { fontSize: 9 },
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50, fillColor: [240, 244, 255] }, 1: { cellWidth: 130 } },
      theme: 'grid'
    });
    const dy = (doc as any).lastAutoTable.finalY + 10;
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.text('Dossiers', 14, dy);
    if (dossiers.length === 0) {
      doc.setFontSize(9);
      doc.setFont('helvetica', 'italic');
      doc.setTextColor(150, 150, 150);
      doc.text('Aucun dossier', 14, dy + 8);
      doc.setTextColor(0, 0, 0);
    } else {
      autoTable(doc, {
        startY: dy + 4,
        head: [['Numero', 'Objet', 'Statut']],
        body: dossiers.map(d => [d.numero_dossier || '', d.objet || '', d.statut || '']),
        styles: { fontSize: 8 },
        headStyles: { fillColor: [30, 58, 95] }
      });
    }
    const py = (doc as any).lastAutoTable?.finalY + 10 || dy + 20;
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.text('Paiements', 14, py);
    if (paiements.length === 0) {
      doc.setFontSize(9);
      doc.setFont('helvetica', 'italic');
      doc.setTextColor(150, 150, 150);
      doc.text('Aucun paiement', 14, py + 8);
    } else {
      const total = paiements.reduce((s: number, p: any) => s + (p.montant || 0), 0);
      autoTable(doc, {
        startY: py + 4,
        head: [['Type', 'Montant (FCFA)', 'Mode', 'Date']],
        body: [
          ...paiements.map((p: any) => [p.type_paiement || '', Number(p.montant || 0).toLocaleString('fr-FR'), p.mode_paiement || '', p.date_paiement ? new Date(p.date_paiement).toLocaleDateString('fr-FR') : '']),
          ['TOTAL', total.toLocaleString('fr-FR') + ' FCFA', '', '']
        ],
        styles: { fontSize: 8 },
        headStyles: { fillColor: [16, 185, 129] }
      });
    }
    doc.save('fiche-client-' + (client.nom || 'client') + '.pdf');
  }

  exportPaiements(paiements: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Paiements');
    autoTable(doc, {
      startY: 48,
      head: [['Dossier', 'Type', 'Montant (FCFA)', 'Mode', 'Date']],
      body: paiements.map(p => [
        p.id_dossier || '',
        p.type_paiement || '',
        p.montant ? Number(p.montant).toLocaleString('fr-FR') : '',
        p.mode_paiement || '',
        p.date_paiement ? new Date(p.date_paiement).toLocaleDateString('fr-FR') : ''
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('paiements.pdf');
  }

  exportJournalPaiements(paiements: any[]) {
    const doc = new jsPDF();
    doc.setFillColor(30, 58, 95);
    doc.rect(0, 0, 210, 35, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(18);
    doc.setFont('helvetica', 'bold');
    doc.text('JOURNAL DE CAISSE', 14, 15);
    doc.setFontSize(11);
    doc.text('Cabinet Me SAWADOGO - Huissier de Justice', 14, 23);
    doc.setFontSize(9);
    doc.text('Genere le : ' + new Date().toLocaleDateString('fr-FR'), 14, 30);
    doc.setTextColor(0, 0, 0);
    const total = paiements.reduce((s, p) => s + (p.montant || 0), 0);
    doc.setFontSize(11);
    doc.setFont('helvetica', 'bold');
    doc.text('Total encaisse : ' + total.toLocaleString('fr-FR') + ' FCFA', 14, 46);
    autoTable(doc, {
      startY: 52,
      head: [['Date', 'Dossier', 'Type', 'Libelle', 'Mode', 'Montant (FCFA)']],
      body: paiements.map(p => [
        p.date_paiement ? new Date(p.date_paiement).toLocaleDateString('fr-FR') : '',
        p.id_dossier || '',
        p.type_paiement || '',
        p.note_caisse || '',
        p.mode_paiement || '',
        Number(p.montant || 0).toLocaleString('fr-FR')
      ]),
      styles: { fontSize: 8 },
      headStyles: { fillColor: [30, 58, 95] },
      foot: [['', '', '', '', 'TOTAL', total.toLocaleString('fr-FR') + ' FCFA']],
      footStyles: { fillColor: [220, 252, 231], fontStyle: 'bold', textColor: [22, 101, 52] }
    });
    doc.save('journal-caisse.pdf');
  }

  imprimerRecuPaiement(paiement: any, dossierLabel: string) {
    const doc = new jsPDF({ format: 'a5' });
    const w = 148;
    doc.setFillColor(30, 58, 95);
    doc.rect(0, 0, w, 30, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(14);
    doc.setFont('helvetica', 'bold');
    doc.text('RECU DE PAIEMENT', w / 2, 13, { align: 'center' });
    doc.setFontSize(9);
    doc.text('Cabinet Me SAWADOGO - Huissier de Justice', w / 2, 21, { align: 'center' });
    doc.setFontSize(8);
    doc.text('Ouagadougou, Burkina Faso', w / 2, 27, { align: 'center' });
    doc.setTextColor(0, 0, 0);
    const numRecu = 'N' + String(paiement.id).padStart(6, '0');
    doc.setFontSize(10);
    doc.setFont('helvetica', 'bold');
    doc.text(numRecu, w - 14, 38, { align: 'right' });
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.text('Date : ' + (paiement.date_paiement ? new Date(paiement.date_paiement).toLocaleDateString('fr-FR') : new Date().toLocaleDateString('fr-FR')), 14, 38);
    doc.setDrawColor(200, 200, 200);
    doc.line(14, 42, w - 14, 42);
    autoTable(doc, {
      startY: 46,
      body: [
        ['Dossier', dossierLabel],
        ['Type', paiement.type_paiement || ''],
        ['Mode', paiement.mode_paiement || ''],
        ['Libelle', paiement.note_caisse || ''],
        ['Reference', paiement.reference || ''],
      ],
      styles: { fontSize: 8 },
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50, fillColor: [240, 244, 255] }, 1: { cellWidth: 80 } },
      theme: 'grid'
    });
    const my = (doc as any).lastAutoTable.finalY + 8;
    doc.setFillColor(240, 253, 244);
    doc.setDrawColor(34, 197, 94);
    doc.roundedRect(14, my, w - 28, 20, 3, 3, 'FD');
    doc.setFontSize(11);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(22, 101, 52);
    doc.text('MONTANT ENCAISSE', w / 2, my + 8, { align: 'center' });
    doc.setFontSize(16);
    doc.text(Number(paiement.montant || 0).toLocaleString('fr-FR') + ' FCFA', w / 2, my + 16, { align: 'center' });
    const sy = my + 30;
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    doc.text('Signature et cachet :', 14, sy);
    doc.setDrawColor(200, 200, 200);
    doc.rect(14, sy + 3, 50, 20);
    const ph = doc.internal.pageSize.height;
    doc.setFontSize(7);
    doc.setTextColor(150, 150, 150);
    doc.text('Ce recu est un document officiel du Cabinet Me SAWADOGO', w / 2, ph - 8, { align: 'center' });
    doc.save('recu-paiement-' + numRecu + '.pdf');
  }

  exportActes(actes: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Actes');
    autoTable(doc, {
      startY: 48,
      head: [['Dossier', 'Type', 'Date', 'Lieu', 'Resultat']],
      body: actes.map(a => [
        a.id_dossier || '',
        a.type_acte || '',
        a.date_acte ? new Date(a.date_acte).toLocaleDateString('fr-FR') : '',
        a.lieu || '',
        a.resultat || ''
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('actes.pdf');
  }

  exportActeDetails(acte: any, dossierNumero: string, dossierObjet: string) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Fiche Acte');
    autoTable(doc, {
      startY: 48,
      body: [
        ['Dossier', dossierNumero + ' - ' + dossierObjet],
        ['Type', acte.type_acte || ''],
        ['Date', acte.date_acte ? new Date(acte.date_acte).toLocaleDateString('fr-FR') : ''],
        ['Lieu', acte.lieu || ''],
        ['Resultat', acte.resultat || ''],
        ['Observations', acte.observations || ''],
      ],
      styles: { fontSize: 9 },
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50, fillColor: [240, 244, 255] }, 1: { cellWidth: 130 } },
      theme: 'grid'
    });
    doc.save('acte-' + (acte.id || '') + '.pdf');
  }

  exportParties(parties: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Parties');
    autoTable(doc, {
      startY: 48,
      head: [['Nom', 'Role', 'Dossier', 'Contact', 'Adresse']],
      body: parties.map(p => [
        p.nom || '',
        p.role || '',
        p.id_dossier || '',
        p.contact || '',
        p.adresse || ''
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('parties.pdf');
  }

  exportFichePartie(partie: any, dossierLabel: string) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Fiche Partie');
    autoTable(doc, {
      startY: 48,
      body: [
        ['Nom complet', partie.nom || ''],
        ['Role', partie.role || ''],
        ['Dossier concerne', dossierLabel],
        ['Contact', partie.contact || ''],
        ['Adresse', partie.adresse || ''],
      ],
      styles: { fontSize: 9 },
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50, fillColor: [240, 244, 255] }, 1: { cellWidth: 130 } },
      theme: 'grid'
    });
    doc.save('fiche-partie-' + (partie.nom || '') + '.pdf');
  }

  exportAffectations(affectations: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Affectations');
    autoTable(doc, {
      startY: 48,
      head: [['Agent', 'Dossier', 'Priorite', 'Statut', 'Date', 'Notes']],
      body: affectations.map(a => [
        a.id_utilisateur || '',
        a.id_dossier || '',
        a.priorite || '',
        a.statut || '',
        a.date_affectation ? new Date(a.date_affectation).toLocaleDateString('fr-FR') : '',
        a.notes || ''
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('affectations.pdf');
  }

  exportDocuments(documents: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Documents');
    autoTable(doc, {
      startY: 48,
      head: [['Nom fichier', 'Type', 'Taille', 'Dossier', 'Date depot']],
      body: documents.map(d => [
        d.nom_original || '',
        d.type_document || '',
        d.taille_lisible || '',
        d.id_dossier ? '#' + d.id_dossier : '',
        d.date_upload ? new Date(d.date_upload).toLocaleDateString('fr-FR') : ''
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('documents.pdf');
  }

  exportFicheDocument(doc_info: any, dossierLabel: string) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Fiche Document');
    autoTable(doc, {
      startY: 48,
      body: [
        ['Nom du fichier', doc_info.nom_original || ''],
        ['Type', doc_info.type_document || ''],
        ['Format', doc_info.mime_type || ''],
        ['Taille', doc_info.taille_lisible || ''],
        ['Dossier', dossierLabel],
        ['Date de depot', doc_info.date_upload ? new Date(doc_info.date_upload).toLocaleDateString('fr-FR') : ''],
        ['Description', doc_info.description || ''],
      ],
      styles: { fontSize: 9 },
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50, fillColor: [240, 244, 255] }, 1: { cellWidth: 130 } },
      theme: 'grid'
    });
    doc.save('fiche-document-' + (doc_info.id || '') + '.pdf');
  }

  exportArchives(archives: any[], dossiers: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Archives');
    const getLabel = (id: number) => {
      const d = dossiers.find((x: any) => x.id === id);
      return d ? (d.numero || d.numero_dossier || '') + ' - ' + (d.objet || '') : '#' + id;
    };
    autoTable(doc, {
      startY: 48,
      head: [['Type', 'Dossier', 'Raison', 'Date archivage', 'Suppression prevue']],
      body: archives.map(a => [
        a.type_archive || '',
        getLabel(a.dossier_id),
        a.raison_archivage || '',
        a.date_archivage ? new Date(a.date_archivage).toLocaleDateString('fr-FR') : '',
        a.date_suppression_prevue ? new Date(a.date_suppression_prevue).toLocaleDateString('fr-FR') : 'Non definie'
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('archives.pdf');
  }

  exportFicheArchive(archive: any, dossierLabel: string) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Fiche Archive');
    autoTable(doc, {
      startY: 48,
      body: [
        ['Type', archive.type_archive || ''],
        ['Dossier', dossierLabel],
        ['Raison archivage', archive.raison_archivage || ''],
        ['Date archivage', archive.date_archivage ? new Date(archive.date_archivage).toLocaleDateString('fr-FR') : ''],
        ['Suppression prevue', archive.date_suppression_prevue ? new Date(archive.date_suppression_prevue).toLocaleDateString('fr-FR') : 'Non definie'],
      ],
      styles: { fontSize: 9 },
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50, fillColor: [240, 244, 255] }, 1: { cellWidth: 130 } },
      theme: 'grid'
    });
    doc.save('fiche-archive-' + (archive.id || '') + '.pdf');
  }

  exportAgendas(agendas: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Agenda - Rendez-vous et Audiences');
    autoTable(doc, {
      startY: 48,
      head: [['Titre', 'Type', 'Date debut', 'Date fin', 'Lieu', 'Statut', 'Priorite']],
      body: agendas.map(a => [
        a.titre || '',
        a.type_rdv || '',
        a.date_debut ? new Date(a.date_debut).toLocaleDateString('fr-FR') + ' ' + new Date(a.date_debut).toLocaleTimeString('fr-FR', {hour: '2-digit', minute: '2-digit'}) : '',
        a.date_fin ? new Date(a.date_fin).toLocaleTimeString('fr-FR', {hour: '2-digit', minute: '2-digit'}) : '',
        a.lieu || '',
        a.statut || '',
        a.priorite || ''
      ]),
      styles: { fontSize: 8 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('agenda.pdf');
  }
  exportCabinets(cabinets: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Cabinets');
    autoTable(doc, {
      startY: 48,
      head: [['Nom', 'Ville', 'Telephone', 'Email', 'Agrement', 'Statut']],
      body: cabinets.map(c => [
        c.nom || '',
        c.ville || '',
        c.telephone || '',
        c.email || '',
        c.numero_agrement || '',
        c.actif ? 'Actif' : 'Inactif'
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('cabinets.pdf');
  }

  exportFicheCabinet(cabinet: any) {
    const doc = new jsPDF();
    doc.setFillColor(30, 58, 95);
    doc.rect(0, 0, 210, 35, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(18);
    doc.setFont('helvetica', 'bold');
    doc.text('FICHE CABINET', 14, 15);
    doc.setFontSize(11);
    doc.text('Cabinet Me SAWADOGO - Huissier de Justice', 14, 23);
    doc.setFontSize(9);
    doc.text('Genere le : ' + new Date().toLocaleDateString('fr-FR'), 14, 30);
    doc.setTextColor(0, 0, 0);
    autoTable(doc, {
      startY: 42,
      body: [
        ['Nom', cabinet.nom || ''],
        ['Raison sociale', cabinet.raison_sociale || ''],
        ['Adresse', cabinet.adresse || ''],
        ['Ville', cabinet.ville || ''],
        ['Telephone', cabinet.telephone || ''],
        ['Email', cabinet.email || ''],
        ['Site web', cabinet.site_web || ''],
        ['N Agrement', cabinet.numero_agrement || ''],
        ['Juridiction', cabinet.juridiction_rattachement || ''],
        ['Chambre dep.', cabinet.chambre_departementale || ''],
        ['Statut', cabinet.actif ? 'Actif' : 'Inactif'],
      ],
      styles: { fontSize: 9 },
      columnStyles: { 0: { fontStyle: 'bold', cellWidth: 50, fillColor: [240, 244, 255] }, 1: { cellWidth: 130 } },
      theme: 'grid'
    });
    doc.save('fiche-cabinet-' + (cabinet.nom || '') + '.pdf');
  }


  exportUtilisateurs(utilisateurs: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Liste des Utilisateurs');
    autoTable(doc, {
      startY: 48,
      head: [['Nom', 'Prenom', 'Email', 'Role', 'Telephone', 'Statut']],
      body: utilisateurs.map(u => [
        u.nom || '',
        u.prenom || '',
        u.email || '',
        u.role || '',
        u.telephone || '',
        u.actif ? 'Actif' : 'Inactif'
      ]),
      styles: { fontSize: 9 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('utilisateurs.pdf');
  }



  exportAuditLogs(logs: any[]) {
    const doc = new jsPDF();
    this.addHeader(doc, 'Journal Audit');
    autoTable(doc, {
      startY: 48,
      head: [['Action', 'Table', 'ID', 'Utilisateur', 'Date', 'Heure']],
      body: logs.map(l => [
        l.action || '',
        l.entity_type || '',
        String(l.entity_id || ''),
        String(l.id_utilisateur || ''),
        l.date_action ? new Date(l.date_action).toLocaleDateString('fr-FR') : '',
        l.date_action ? new Date(l.date_action).toLocaleTimeString('fr-FR') : ''
      ]),
      styles: { fontSize: 8 },
      headStyles: { fillColor: [30, 58, 95] }
    });
    doc.save('audit-log.pdf');
  }

}