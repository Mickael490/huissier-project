import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { TagModule } from 'primeng/tag';
import { MessageService, ConfirmationService } from 'primeng/api';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { InputTextModule } from 'primeng/inputtext';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { PdfService } from 'src/services/pdf.service';

@Component({
  selector: 'app-partie',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    DialogModule, ToastModule, TagModule, ConfirmDialogModule, InputTextModule
  ],
  templateUrl: './partie.component.html',
  providers: [MessageService, ConfirmationService]
})
export class PartieComponent implements OnInit {
  parties = signal<any[]>([]);
  dossiers: any[] = [];
  partie: any = {};
  partieSelectionnee: any = null;
  partieDialog = false;
  detailsDialog = false;
  submitted = false;
  isEditMode = false;
  private apiUrl = `${environment.apiUrl}/parties`;

  roleOptions = [
    { label: 'Débiteur', value: 'debiteur' },
    { label: 'Destinataire / Créancier', value: 'destinataire' },
    { label: 'Autre', value: 'autre' }
  ];

  constructor(
    private http: HttpClient,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadParties();
    this.loadDossiers();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  loadDossiers(): void {
    this.http.get<any>(`${environment.apiUrl}/dossiers`, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.dossiers = data.dossiers || [],
      error: () => {}
    });
  }

  loadParties(): void {
    this.http.get<any[]>(this.apiUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.parties.set(data),
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
    });
  }

  openNew(): void {
    this.partie = { role: 'debiteur' };
    this.isEditMode = false;
    this.partieDialog = true;
    this.submitted = false;
  }

  editPartie(partie: any): void {
    this.partie = { ...partie };
    this.isEditMode = true;
    this.partieDialog = true;
  }

  voirDetails(partie: any): void {
    this.partieSelectionnee = partie;
    this.detailsDialog = true;
  }

  editFromDetails(): void {
    this.detailsDialog = false;
    this.editPartie(this.partieSelectionnee);
  }

  hideDialog(): void {
    this.partieDialog = false;
    this.submitted = false;
  }

  savePartie(): void {
    this.submitted = true;
    if (!this.partie.nom || !this.partie.id_dossier) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Veuillez remplir les champs obligatoires' });
      return;
    }
    if (this.isEditMode && this.partie.id) {
      this.http.put(`${this.apiUrl}/${this.partie.id}`, this.partie, { headers: this.getHeaders() }).subscribe({
        next: () => {
          this.loadParties();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Partie mise à jour' });
          this.hideDialog();
        },
        error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
      });
    } else {
      this.http.post(this.apiUrl, this.partie, { headers: this.getHeaders() }).subscribe({
        next: () => {
          this.loadParties();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Partie créée' });
          this.hideDialog();
        },
        error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
      });
    }
  }

  deletePartie(partie: any): void {
    this.confirmationService.confirm({
      message: `Supprimer la partie ${partie.nom} ?`,
      accept: () => {
        this.http.delete(`${this.apiUrl}/${partie.id}`, { headers: this.getHeaders() }).subscribe({
          next: () => {
            this.loadParties();
            this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Partie supprimée' });
          },
          error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
        });
      }
    });
  }

  getDossierLabel(id: number): string {
    const d = this.dossiers.find(x => x.id === id);
    return d ? `${d.numero_dossier} — ${d.objet}` : `#${id}`;
  }

  getRoleSeverity(role: string): string {
    switch (role) {
      case 'debiteur': return 'danger';
      case 'destinataire': return 'info';
      default: return 'secondary';
    }
  }

  getRoleLabel(role: string): string {
    switch (role) {
      case 'debiteur': return 'Débiteur';
      case 'destinataire': return 'Créancier';
      default: return 'Autre';
    }
  }

  getNombreDebiteurs(): number {
    return this.parties().filter(p => p.role === 'debiteur').length;
  }

  getNombreDestinataires(): number {
    return this.parties().filter(p => p.role === 'destinataire').length;
  }

  getNombreAutres(): number {
    return this.parties().filter(p => p.role === 'autre').length;
  }

  onGlobalFilter(table: any, event: Event): void {
    table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
  }

  exportListePDF(): void {
    this.pdfService.exportParties(this.parties());
  }

  exportFichePartiePDF(): void {
    if (this.partieSelectionnee) {
      this.pdfService.exportFichePartie(
        this.partieSelectionnee,
        this.getDossierLabel(this.partieSelectionnee.id_dossier)
      );
    }
  }
}