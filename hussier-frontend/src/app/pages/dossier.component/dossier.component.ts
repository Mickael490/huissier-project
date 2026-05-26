import { PdfService } from 'src/services/pdf.service';
import { Component, OnInit, ViewChild, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Table, TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { ToolbarModule } from 'primeng/toolbar';
import { InputTextModule } from 'primeng/inputtext';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { CheckboxModule } from 'primeng/checkbox';
import { MessageService, ConfirmationService } from 'primeng/api';
import { DossierService } from 'src/services/dossiers/DossierService';
import { Dossier, DossierCreate, DossierUpdate, StatutDossier, TypeDossier } from 'src/types/dossier';
import { TagModule } from 'primeng/tag';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-dossier',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    DialogModule, ToastModule, ToolbarModule, InputTextModule,
    ConfirmDialogModule, CheckboxModule, TagModule
  ],
  templateUrl: './dossier.component.html',
  providers: [MessageService, ConfirmationService]
})
export class DossierComponent implements OnInit {

  dossiers = signal<Dossier[]>([]);
  dossier: any = {};
  selectedDossiers: Dossier[] = [];
  dossierDialog = false;
  detailsDialog = false;
  motDePasseDialog = false;
  submitted = false;
  isEditMode = false;
  dossierSelectionne: any = null;
  motDePasseSaisi = '';
  dossierEnAttente: any = null;
  protegerParMotDePasse = false;
  dossiersDeverrouilles = new Set<number>();

  filterCabinetId?: number;
  filterClientId?: number;
  filterStatut?: StatutDossier;
  filterType?: TypeDossier;

  @ViewChild('dt') dt!: Table;

  cabinets: any[] = [];
  clients: any[] = [];
  utilisateurs: any[] = [];

  statutOptions = [
    { label: 'Nouveau', value: StatutDossier.NOUVEAU },
    { label: 'En cours', value: StatutDossier.EN_COURS },
    { label: 'En attente', value: StatutDossier.EN_ATTENTE },
    { label: 'Terminé', value: StatutDossier.TERMINE },
    { label: 'Archivé', value: StatutDossier.ARCHIVE },
    { label: 'Annulé', value: StatutDossier.ANNULE }
  ];

  typeOptions = [
    { label: 'Contentieux', value: TypeDossier.CONTENTIEUX },
    { label: 'Recouvrement', value: TypeDossier.RECOUVREMENT },
    { label: 'Constat', value: TypeDossier.CONSTAT },
    { label: 'Signification', value: TypeDossier.SIGNIFICATION },
    { label: 'Saisie', value: TypeDossier.SAISIE },
    { label: 'Expulsion', value: TypeDossier.EXPULSION },
    { label: 'Autre', value: TypeDossier.AUTRE }
  ];

  constructor(
    private dossierService: DossierService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadDossiers();
    this.loadDropdowns();
  }

  loadDropdowns(): void {
    this.dossierService.getCabinets().subscribe({
      next: (data: any[]) => this.cabinets = data,
      error: (err: any) => console.error('Erreur cabinets:', err)
    });
    this.dossierService.getClients().subscribe({
      next: (data: any[]) => this.clients = data,
      error: (err: any) => console.error('Erreur clients:', err)
    });
    this.dossierService.getUtilisateurs().subscribe({
      next: (data: any[]) => this.utilisateurs = data,
      error: (err: any) => console.error('Erreur utilisateurs:', err)
    });
  }

  openNew(): void {
    this.isEditMode = false;
    this.protegerParMotDePasse = false;
    this.dossier = {
      objet: '',
      description: '',
      type_dossier: TypeDossier.CONTENTIEUX,
      statut: StatutDossier.NOUVEAU,
      montant_principal: 0,
      montant_frais: 0,
      client_id: undefined,
      cabinet_id: undefined,
      date_ouverture: this.getTodayDateString()
    };
    this.dossierDialog = true;
    this.submitted = false;
  }

  editDossier(dossier: any): void {
    this.isEditMode = true;
    this.protegerParMotDePasse = !!dossier.mot_de_passe;
    this.dossier = { ...dossier };
    this.dossierDialog = true;
  }

  hideDialog(): void {
    this.dossierDialog = false;
    this.submitted = false;
    this.isEditMode = false;
  }

  calculerMontantTotal(): void {
    const principal = Number(this.dossier.montant_principal) || 0;
    const frais = Number(this.dossier.montant_frais) || 0;
    this.dossier.montant_total = principal + frais;
  }

  saveDossier(): void {
    this.submitted = true;
    if (!this.dossier.objet || !this.dossier.type_dossier || !this.dossier.cabinet_id) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Veuillez remplir tous les champs obligatoires' });
      return;
    }
    if (!this.protegerParMotDePasse) {
      this.dossier.mot_de_passe = undefined;
    }
    if (this.isEditMode && this.dossier.id) {
      this.dossierService.updateDossier(this.dossier.id, this.dossier).subscribe({
        next: () => {
          this.loadDossiers();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Dossier mis à jour' });
          this.hideDialog();
        },
        error: (err: any) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: err.error?.detail || 'Erreur mise à jour' })
      });
    } else {
      this.dossierService.createDossier(this.dossier).subscribe({
        next: (response: any) => {
          this.loadDossiers();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: `Dossier ${response.numero_dossier} créé avec succès` });
          this.hideDialog();
        },
        error: (err: any) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: err.error?.detail || 'Erreur création' })
      });
    }
  }

  deleteDossier(dossier: any): void {
    this.confirmationService.confirm({
      message: `Voulez-vous vraiment supprimer le dossier ${dossier.numero_dossier} ?`,
      accept: () => {
        this.dossierService.deleteDossier(dossier.id!).subscribe({
          next: () => {
            this.loadDossiers();
            this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Dossier supprimé' });
          },
          error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur lors de la suppression' })
        });
      }
    });
  }

  deleteSelectedDossiers(): void {
    this.confirmationService.confirm({
      message: `Supprimer les ${this.selectedDossiers.length} dossiers sélectionnés ?`,
      header: 'Confirmation',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        const dossiersAvecId = this.selectedDossiers.filter(d => d.id !== undefined);
        if (dossiersAvecId.length === 0) return;
        const deleteObservables = dossiersAvecId.map(d => this.dossierService.deleteDossier(d.id!));
        forkJoin(deleteObservables).subscribe({
          next: () => {
            this.selectedDossiers = [];
            this.loadDossiers();
            this.messageService.add({ severity: 'success', summary: 'Supprimé', detail: `${dossiersAvecId.length} dossier(s) supprimé(s)` });
          },
          error: () => {
            this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Impossible de supprimer certains dossiers' });
            this.loadDossiers();
          }
        });
      }
    });
  }

  loadDossiers(): void {
    this.dossierService.getDossiers(0, 100, this.filterCabinetId, this.filterClientId, this.filterStatut, this.filterType).subscribe({
      next: (response: any) => this.dossiers.set(response.dossiers),
      error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur lors du chargement des dossiers' })
    });
  }

  voirDetails(dossier: any): void {
    if (dossier.mot_de_passe && !this.dossiersDeverrouilles.has(dossier.id)) {
      this.dossierEnAttente = dossier;
      this.motDePasseSaisi = '';
      this.motDePasseDialog = true;
    } else {
      this.dossierSelectionne = dossier;
      this.detailsDialog = true;
    }
  }

  verifierMotDePasse(): void {
    if (this.motDePasseSaisi === this.dossierEnAttente?.mot_de_passe) {
      this.dossiersDeverrouilles.add(this.dossierEnAttente.id);
      this.dossierSelectionne = this.dossierEnAttente;
      this.motDePasseDialog = false;
      this.detailsDialog = true;
      this.motDePasseSaisi = '';
    } else {
      this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Mot de passe incorrect' });
    }
  }

  editFromDetails(): void {
    this.detailsDialog = false;
    this.editDossier(this.dossierSelectionne);
  }

  exportDossierPDF(): void {
    if (this.dossierSelectionne) {
      this.pdfService.exportDossiers([this.dossierSelectionne]);
    }
  }

  getClientNom(clientId: number): string {
    const client = this.clients.find((c: any) => c.id === clientId);
    return client ? `${client.nom} ${client.prenom || ''}`.trim() : '-';
  }

  getClientNomComplet(clientId: number): string {
    return this.getClientNom(clientId);
  }

  getResponsableNomComplet(utilisateurId?: number): string {
    if (!utilisateurId) return '-';
    const u = this.utilisateurs.find((u: any) => u.id === utilisateurId);
    return u ? u.nom : '-';
  }

  onGlobalFilter(table: Table, event: Event): void {
    table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
  }

  exportCSV(): void {
    if (this.dt) this.dt.exportCSV({ selectionOnly: true });
  }

  exportPDF(): void {
    this.pdfService.exportDossiers(this.dossiers());
  }

  private getTodayDateString(): string {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  getStatutSeverity(statut: string): string {
    switch (statut) {
      case 'nouveau': return 'info';
      case 'en_cours': return 'warning';
      case 'termine': return 'success';
      case 'archive': return 'secondary';
      case 'annule': return 'danger';
      default: return 'info';
    }
  }
}
