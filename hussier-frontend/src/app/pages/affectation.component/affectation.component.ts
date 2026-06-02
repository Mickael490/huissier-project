import { Component, OnInit, signal, ViewChild, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
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

@Component({
  selector: 'app-affectation',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    ButtonModule,
    DialogModule,
    ToastModule,
    InputTextModule,
    ConfirmDialogModule,
    TagModule,
    TextareaModule
  ],
  providers: [MessageService, ConfirmationService],
  templateUrl: './affectation.component.html'
})
export class AffectationComponent implements OnInit {
  
  affectations = signal<any[]>([]);
  actes = signal<any[]>([]);
  dossiers: { id: number; numero: string; objet: string }[] = [];
  utilisateurs: { id: number; nom: string; role: string }[] = [];
  
  affectation: any = {};
  affectationDialog = false;
  detailsDialog = false;
  submitted = false;
  isEditMode = false;
  
  affectationSelectionnee: any = null;
  get affectationSelectionne(): any {
    return this.affectationSelectionnee;
  }
  set affectationSelectionne(value: any) {
    this.affectationSelectionnee = value;
  }

  @ViewChild('dt') dt!: Table;

  readonly nbEnCours = computed(() => this.affectations().filter(a => a.statut === 'en_cours').length);
  readonly nbTerminees = computed(() => this.affectations().filter(a => a.statut === 'termine').length);
  readonly nbUrgentes = computed(() => this.affectations().filter(a => a.priorite === 'haute' && a.statut === 'en_cours').length);

  get actesDisponibles(): any[] {
    const listAffectations = this.affectations();
    return this.actes().filter(acte => {
      if (this.isEditMode && this.affectation?.id_acte === acte.id) {
        return true;
      }
      return !listAffectations.some(aff => aff.id_acte === acte.id && aff.statut !== 'annule');
    });
  }

  private apiUrl = `${environment.apiUrl}/affectations`;
  private acteUrl = `${environment.apiUrl}/actes`;
  private dossierUrl = `${environment.apiUrl}/dossiers`;
  private utilisateurUrl = `${environment.apiUrl}/utilisateurs`;

  typeOptions = [
    { label: 'Normale', value: 'normale' },
    { label: 'Haute / Urgente', value: 'haute' }
  ];

  constructor(
    private http: HttpClient,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadAffectations();
    this.loadActes();
    this.loadDossiers();
    this.loadUtilisateurs();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  loadActes(): void {
    this.http.get<any[]>(this.acteUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => {
        console.log("DEBUG: Actes chargés =", data);
        this.actes.set((data || []).map((a: any) => ({
          id: a.id, type_acte: a.type_acte, id_dossier: a.id_dossier
        })));
        console.log("DEBUG: actes.signal =", this.actes());
      },
      error: (err) => console.error('Erreur actes:', err)
    });
  }

  loadDossiers(): void {
    this.http.get<any>(this.dossierUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => {
        this.dossiers = (data.dossiers || []).map((d: any) => ({
          id: d.id, numero: d.numero_dossier, objet: d.objet
        }));
      },
      error: () => {}
    });
  }

  loadUtilisateurs(): void {
    this.http.get<any[]>(this.utilisateurUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => {
        this.utilisateurs = data.map((u: any) => ({
          id: u.id, nom: `${u.prenom} ${u.nom}`, role: u.role
        }));
      },
      error: () => {}
    });
  }

  loadAffectations(): void {
    this.http.get<any[]>(this.apiUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.affectations.set(data),
      error: () => this.messageService.add({
        severity: 'error', summary: 'Erreur', detail: 'Erreur lors du chargement des affectations'
      })
    });
  }

  openNew(): void {
    this.affectation = {
      priorite: 'normale',
      statut: 'en_cours',
      date_affectation: new Date().toISOString().split('T')[0]
    };
    this.isEditMode = false;
    this.affectationDialog = true;
    this.submitted = false;
  }

  editAffectation(affectation: any): void {
    this.affectation = { ...affectation };
    if (this.affectation.date_affectation) {
      this.affectation.date_affectation = this.affectation.date_affectation.split('T')[0];
    }
    this.isEditMode = true;
    this.affectationDialog = true;
  }

  voirDetails(affectation: any): void {
    this.affectationSelectionnee = affectation;
    this.detailsDialog = true;
  }

  editFromDetails(): void {
    this.detailsDialog = false;
    this.editAffectation(this.affectationSelectionnee);
  }

  hideDialog(): void {
    this.affectationDialog = false;
    this.submitted = false;
  }

  saveAffectation(): void {
    this.submitted = true;
    if (!this.affectation.id_acte || !this.affectation.id_utilisateur || !this.affectation.date_affectation) {
      this.messageService.add({
        severity: 'warn', summary: 'Attention', detail: 'Veuillez remplir les champs obligatoires'
      });
      return;
    }

    if (this.isEditMode && this.affectation.id) {
      this.http.put(`${this.apiUrl}/${this.affectation.id}`, this.affectation, { headers: this.getHeaders() }).subscribe({
        next: () => {
          this.loadAffectations();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Affectation mise à jour' });
          this.hideDialog();
        },
        error: (err) => this.messageService.add({
          severity: 'error', summary: 'Erreur', detail: err.error?.detail || 'Erreur mise à jour'
        })
      });
    } else {
      this.http.post(this.apiUrl, this.affectation, { headers: this.getHeaders() }).subscribe({
        next: () => {
          this.loadAffectations();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Acte affecté avec succès' });
          this.hideDialog();
        },
        error: (err) => this.messageService.add({
          severity: 'error', summary: 'Erreur', detail: err.error?.detail || 'Erreur création'
        })
      });
    }
  }

  supprimerAffectation(affectation: any): void {
    this.confirmationService.confirm({
      message: `Voulez-vous vraiment annuler cette affectation de mission ?`,
      header: 'Retrait de mission',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        this.http.delete(`${this.apiUrl}/${affectation.id}`, { headers: this.getHeaders() }).subscribe({
          next: () => {
            this.loadAffectations();
            this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Affectation retirée' });
          },
          error: (err) => this.messageService.add({
            severity: 'error', summary: 'Erreur', detail: err.error?.detail || 'Erreur suppression'
          })
        });
      }
    });
  }

  exportListePDF(): void {
    this.pdfService.exportAffectations(this.affectations());
  }

  onGlobalFilter(table: Table, event: Event): void {
    table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
  }

  getActeLabel(id: number): string {
    const a = this.actes().find(x => x.id === id);
    if (!a) return `Acte #${id}`;
    switch (a.type_acte) {
      case 'SIGNIFICATION': return 'Signification';
      case 'CONSTAT': return 'Constat';
      case 'SAISIE': return 'Saisie';
      case 'RECOUVREMENT': return 'Recouvrement';
      case 'EXPULSION': return 'Expulsion';
      case 'COMMANDEMENT': return 'Commandement';
      case 'PROCES_VERBAL': return 'Procès Verbal';
      case 'INVENTAIRE': return 'Inventaire';
      case 'AUTRE': return 'Autre';
      default: return a.type_acte;
    }
  }

  getDossierNumeroParActe(idActe: number): string {
    const a = this.actes().find(x => x.id === idActe);
    if (!a) return '—';
    const d = this.dossiers.find(x => x.id === a.id_dossier);
    return d ? d.numero : '—';
  }

  getUtilisateurNom(id: number): string {
    const u = this.utilisateurs.find(x => x.id === id);
    return u ? u.nom : `Agent #${id}`;
  }

  getPrioriteLabel(priorite: string): string {
    return priorite === 'haute' ? 'Urgente' : 'Normale';
  }

  getPrioriteSeverity(priorite: string): string {
    return priorite === 'haute' ? 'danger' : 'info';
  }

  getStatutLabel(statut: string): string {
    switch (statut) {
      case 'en_cours': return 'En cours';
      case 'termine': return 'Terminé';
      case 'annule': return 'Annulé';
      default: return statut;
    }
  }

  getStatutSeverity(statut: string): string {
    switch (statut) {
      case 'en_cours': return 'warning';
      case 'termine': return 'success';
      case 'annule': return 'danger';
      default: return 'secondary';
    }
  }
}

