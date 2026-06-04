import { Component, OnInit, signal, ViewChild, computed } from '@angular/core';
import { CommonModule, registerLocaleData } from '@angular/common';
import localeFr from '@angular/common/locales/fr';
import { FormsModule } from '@angular/forms';
import { Table, TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { InputTextModule } from 'primeng/inputtext';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { TagModule } from 'primeng/tag';
import { TextareaModule } from 'primeng/textarea';
import { MessageService, ConfirmationService } from 'primeng/api';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { PdfService } from 'src/services/pdf.service';

registerLocaleData(localeFr, 'fr-FR');

@Component({
  selector: 'app-paiement',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    DialogModule, ToastModule, InputTextModule,
    ConfirmDialogModule, TagModule, TextareaModule
  ],
  providers: [MessageService, ConfirmationService],
  templateUrl: './paiement.component.html'
})
export class PaiementComponent implements OnInit {

  paiements = signal<any[]>([]);
  dossiers: { id: number; numero: string; objet: string }[] = [];
  paiement: any = {};
  paiementDialog = false;
  detailsDialog = false;
  submitted = false;
  isEditMode = false;
  paiementSelectionne: any = null;
  motDePasseDialog = false;
  motDePasseSaisi = '';
  paiementEnAttente: any = null;
  paiementsDeverrouilles = new Set<number>();
  protegerParMotDePasse = false;

  @ViewChild('dt') dt!: Table;

  readonly totalEncaisse = computed(() =>
    this.paiements().reduce((s, p) => s + (p.montant || 0), 0)
  );

  readonly totalEnAttente = computed(() =>
    this.paiements().filter(p => p.statut === 'attente').length
  );

  readonly moyennePaiement = computed(() => {
    const list = this.paiements();
    if (!list.length) return 0;
    return list.reduce((s, p) => s + (p.montant || 0), 0) / list.length;
  });

  private apiUrl = `${environment.apiUrl}/paiements`;
  private dossierUrl = `${environment.apiUrl}/dossiers`;

  modeOptions = [
    { label: 'Espèces', value: 'especes', icon: 'pi pi-money-bill' },
    { label: 'Chèque', value: 'cheque', icon: 'pi pi-file' },
    { label: 'Virement', value: 'virement', icon: 'pi pi-arrow-right-arrow-left' },
    { label: 'Mobile Money', value: 'mobile', icon: 'pi pi-mobile' },
    { label: 'Autre', value: 'autre', icon: 'pi pi-wallet' }
  ];

  reseauxMobile = [
    { label: 'Orange Money', value: 'orange', icon: 'pi pi-circle-fill', color: '#ff7900' },
    { label: 'MTN Mobile Money', value: 'mtn', icon: 'pi pi-circle-fill', color: '#ffcc00' },
    { label: 'Moov Money', value: 'moov', icon: 'pi pi-circle-fill', color: '#0066b3' },
    { label: 'Wave', value: 'wave', icon: 'pi pi-circle-fill', color: '#1dc8f5' },
    { label: 'Coris Money', value: 'coris', icon: 'pi pi-circle-fill', color: '#e30613' }
  ];

  typeOptions = [
    { label: 'Acompte', value: 'acompte' },
    { label: 'Provision', value: 'provision' },
    { label: 'Solde', value: 'solde' },
    { label: 'Frais', value: 'frais' },
    { label: 'Recouvrement', value: 'recouvrement' },
    { label: 'Autre', value: 'autre' }
  ];

  constructor(
    private http: HttpClient,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadPaiements();
    this.loadDossiers();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  loadDossiers(): void {
    this.http.get<any>(this.dossierUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.dossiers = (data.dossiers || []).map((d: any) => ({
        id: d.id, numero: d.numero_dossier, objet: d.objet
      })),
      error: () => {}
    });
  }

  loadPaiements(): void {
    this.http.get<any>(this.apiUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.paiements.set(data.paiements || data),
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
    });
  }

  openNew(): void {
    const today = new Date().toISOString().substring(0, 10);
    this.paiement = {
      mode_paiement: 'especes',
      type_paiement: '',
      date_paiement: today,
      reverse_au_client: false
    };
    this.protegerParMotDePasse = false;
    this.isEditMode = false;
    this.paiementDialog = true;
    this.submitted = false;
  }

  editPaiement(paiement: any): void {
    this.paiement = { ...paiement };
    this.protegerParMotDePasse = !!paiement.mot_de_passe;
    this.isEditMode = true;
    this.paiementDialog = true;
  }

  voirDetails(paiement: any): void {
    if (paiement.mot_de_passe && !this.paiementsDeverrouilles.has(paiement.id)) {
      this.paiementEnAttente = paiement;
      this.motDePasseSaisi = '';
      this.motDePasseDialog = true;
    } else {
      this.paiementSelectionne = paiement;
      this.detailsDialog = true;
    }
  }

  verifierMotDePasse(): void {
    if (this.motDePasseSaisi === this.paiementEnAttente?.mot_de_passe) {
      this.paiementsDeverrouilles.add(this.paiementEnAttente.id);
      this.paiementSelectionne = this.paiementEnAttente;
      this.motDePasseDialog = false;
      this.detailsDialog = true;
      this.motDePasseSaisi = '';
    } else {
      this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Mot de passe incorrect' });
      this.motDePasseSaisi = '';
    }
  }

  editFromDetails(): void {
    this.detailsDialog = false;
    this.editPaiement(this.paiementSelectionne);
  }

  hideDialog(): void {
    this.paiementDialog = false;
    this.submitted = false;
  }

  savePaiement(): void {
    this.submitted = true;
    if (!this.protegerParMotDePasse) {
      this.paiement.mot_de_passe = null;
    }
    if (
      !this.paiement.id_dossier ||
      !this.paiement.montant ||
      !this.paiement.type_paiement ||
      !this.paiement.date_paiement ||
      !this.paiement.mode_paiement
    ) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Veuillez remplir les champs obligatoires' });
      return;
    }
    this.paiement.montant = Number(this.paiement.montant);
    if (this.isEditMode && this.paiement.id) {
      this.http.put(`${this.apiUrl}/${this.paiement.id}`, this.paiement, { headers: this.getHeaders() }).subscribe({
        next: () => {
          this.loadPaiements();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Paiement mis à jour' });
          this.hideDialog();
        },
        error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
      });
    } else {
      this.http.post(this.apiUrl, this.paiement, { headers: this.getHeaders() }).subscribe({
        next: () => {
          this.loadPaiements();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Paiement enregistré' });
          this.hideDialog();
        },
        error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
      });
    }
  }

  deletePaiement(paiement: any): void {
    this.confirmationService.confirm({
      message: `Supprimer ce paiement de ${paiement.montant} FCFA ?`,
      accept: () => {
        this.http.delete(`${this.apiUrl}/${paiement.id}`, { headers: this.getHeaders() }).subscribe({
          next: () => {
            this.loadPaiements();
            this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Paiement supprimé' });
          },
          error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
        });
      }
    });
  }

  getDossierLabel(id: number): string {
    const d = this.dossiers.find(x => x.id === id);
    return d ? `${d.numero} — ${d.objet}` : `#${id}`;
  }

  getDossierObjet(id: number): string {
    return this.getDossierLabel(id);
  }

  getTypeLabel(type: string): string {
    const t = this.typeOptions.find(x => x.value === type);
    return t ? t.label : type;
  }

  getTypeSeverity(type: string): string {
    switch (type) {
      case 'acompte': return 'info';
      case 'provision': return 'warning';
      case 'solde': return 'success';
      case 'frais': return 'danger';
      case 'recouvrement': return 'secondary';
      default: return 'info';
    }
  }

  getModeLabel(mode: string): string {
    const m = this.modeOptions.find(x => x.value === mode);
    return m ? m.label : mode;
  }

  getModeIcon(mode: string): string {
    const m = this.modeOptions.find(x => x.value === mode);
    return m ? m.icon : 'pi pi-wallet';
  }

  getModeStyle(mode: string): string {
    switch (mode) {
      case 'especes': return 'background:#dcfce7; color:#16a34a;';
      case 'cheque': return 'background:#dbeafe; color:#1d4ed8;';
      case 'virement': return 'background:#ede9fe; color:#7c3aed;';
      case 'mobile': return 'background:#fef3c7; color:#d97706;';
      default: return 'background:#f1f5f9; color:#64748b;';
    }
  }

  onGlobalFilter(table: Table, event: Event): void {
    table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
  }

  imprimerRecu(paiement: any): void {
    const dossierLabel = this.getDossierLabel(paiement.id_dossier);
    this.pdfService.imprimerRecuPaiement(paiement, dossierLabel);
  }

  exportExcel(): void {
    this.pdfService.exportJournalPaiements(this.paiements());
  }
}
