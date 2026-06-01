import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
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
  selector: 'app-archive',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    DialogModule, ToastModule, InputTextModule,
    ConfirmDialogModule, TagModule, TextareaModule
  ],
  templateUrl: './archive.component.html',
  providers: [MessageService, ConfirmationService]
})
export class ArchiveComponent implements OnInit {
  archives = signal<any[]>([]);
  dossiers: { id: number; numero: string; objet: string }[] = [];
  archive: any = {};
  archiveDialog = false;
  detailsDialog = false;
  submitted = false;
  archiveSelectionnee: any = null;
  motDePasseDialog = false;
  motDePasseSaisi = '';
  archiveEnAttente: any = null;
  archivesDeverrouillees = new Set<number>();
  protegerParMotDePasse = false;
  private apiUrl = `${environment.apiUrl}/archives`;

  readonly totalArchives = computed(() => this.archives().length);
  readonly archivesDossier = computed(() => this.archives().filter(a => a.type_archive === 'DOSSIER').length);
  readonly archivesActe = computed(() => this.archives().filter(a => a.type_archive === 'ACTE').length);

  typeOptions = [
    { label: 'Dossier', value: 'DOSSIER', icon: 'pi pi-folder', color: '#4f46e5' },
    { label: 'Acte', value: 'ACTE', icon: 'pi pi-file-edit', color: '#f97316' },
    { label: 'Document', value: 'DOCUMENT', icon: 'pi pi-file', color: '#10b981' },
    { label: 'Paiement', value: 'PAIEMENT', icon: 'pi pi-dollar', color: '#ef4444' }
  ];

  constructor(
    private http: HttpClient,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadArchives();
    this.loadDossiers();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  loadDossiers(): void {
    this.http.get<any>(`${environment.apiUrl}/dossiers`, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.dossiers = (data.dossiers || []).map((d: any) => ({ id: d.id, numero: d.numero_dossier, objet: d.objet })),
      error: () => {}
    });
  }

  loadArchives(): void {
    this.http.get<any[]>(this.apiUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.archives.set(data),
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur chargement archives' })
    });
  }

  openNew(): void {
    this.archive = { type_archive: 'DOSSIER', id_cabinet: 1 };
    this.protegerParMotDePasse = false;
    this.archiveDialog = true;
    this.submitted = false;
  }

  editArchive(archive: any): void {
    this.archive = { ...archive };
    this.protegerParMotDePasse = !!archive.mot_de_passe;
    this.archiveDialog = true;
  }

  voirDetails(archive: any): void {
    if (archive.mot_de_passe && !this.archivesDeverrouillees.has(archive.id)) {
      this.archiveEnAttente = archive;
      this.motDePasseSaisi = '';
      this.motDePasseDialog = true;
    } else {
      this.archiveSelectionnee = archive;
      this.detailsDialog = true;
    }
  }

  verifierMotDePasse(): void {
    if (this.motDePasseSaisi === this.archiveEnAttente?.mot_de_passe) {
      this.archivesDeverrouillees.add(this.archiveEnAttente.id);
      this.archiveSelectionnee = this.archiveEnAttente;
      this.motDePasseDialog = false;
      this.detailsDialog = true;
      this.motDePasseSaisi = '';
    } else {
      this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Mot de passe incorrect' });
      this.motDePasseSaisi = '';
    }
  }

  hideDialog(): void {
    this.archiveDialog = false;
    this.submitted = false;
  }

  getDossierLabel(id: number): string {
    const d = this.dossiers.find(x => x.id === id);
    return d ? `${d.numero} — ${d.objet}` : `#${id}`;
  }

  getTypeInfo(type: string): any {
    return this.typeOptions.find(t => t.value === type) || this.typeOptions[0];
  }

  getTypeLabel(type: string): string {
    return this.getTypeInfo(type)?.label || type;
  }

  getTypeSeverity(type: string): string {
    switch (type) {
      case 'DOSSIER': return 'info';
      case 'ACTE': return 'warning';
      case 'DOCUMENT': return 'success';
      case 'PAIEMENT': return 'danger';
      default: return 'secondary';
    }
  }

  saveArchive(): void {
    this.submitted = true;
    if (!this.protegerParMotDePasse) {
      this.archive.mot_de_passe = null;
    }
    if (!this.archive.dossier_id || !this.archive.type_archive) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Veuillez remplir les champs obligatoires' });
      return;
    }
    if (this.archive.id) {
      this.http.put(`${this.apiUrl}/${this.archive.id}`, this.archive, { headers: this.getHeaders() }).subscribe({
        next: () => {
          this.loadArchives();
          this.messageService.add({ severity: 'success', summary: 'Succes', detail: 'Archive mise a jour' });
          this.hideDialog();
        },
        error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
      });
      return;
    }
    const payload = {
      dossier_id: this.archive.dossier_id,
      type_archive: this.archive.type_archive,
      id_reference: this.archive.dossier_id,
      id_cabinet: 1,
      donnees_json: { dossier_id: this.archive.dossier_id },
      raison_archivage: this.archive.raison_archivage || 'Archivage manuel',
      archive_par: 2,
      date_suppression_prevue: this.archive.date_suppression_prevue
    };
    this.http.post(this.apiUrl, payload, { headers: this.getHeaders() }).subscribe({
      next: () => {
        this.loadArchives();
        this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Archive créée avec succès' });
        this.hideDialog();
      },
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
    });
  }

  deleteArchive(archive: any): void {
    this.confirmationService.confirm({
      message: `Supprimer définitivement cette archive ?`,
      header: 'Suppression définitive',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        this.http.delete(`${this.apiUrl}/${archive.id}`, { headers: this.getHeaders() }).subscribe({
          next: () => {
            this.loadArchives();
            this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Archive supprimée' });
          },
          error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
        });
      }
    });
  }

  exportListePDF(): void {
    this.pdfService.exportArchives(this.archives(), this.dossiers);
  }

  exportFicheArchivePDF(): void {
    if (this.archiveSelectionnee) {
      this.pdfService.exportFicheArchive(
        this.archiveSelectionnee,
        this.getDossierLabel(this.archiveSelectionnee.dossier_id)
      );
    }
  }
}
