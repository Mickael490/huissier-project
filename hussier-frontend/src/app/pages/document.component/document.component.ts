import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { InputTextModule } from 'primeng/inputtext';
import { ToolbarModule } from 'primeng/toolbar';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { TagModule } from 'primeng/tag';
import { TextareaModule } from 'primeng/textarea';
import { MessageService, ConfirmationService } from 'primeng/api';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { PdfService } from 'src/services/pdf.service';

@Component({
  selector: 'app-document',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    DialogModule, ToastModule, InputTextModule,
    ConfirmDialogModule, TagModule, TextareaModule, ToolbarModule
  ],
  templateUrl: './document.component.html',
  providers: [MessageService, ConfirmationService]
})
export class DocumentComponent implements OnInit {
  documents = signal<any[]>([]);
  dossiers: { id: number; numero: string; objet: string }[] = [];
  documentDialog = false;
  detailsDialog = false;
  submitted = false;
  selectedFile: File | null = null;
  typeDocument = 'acte';
  dossierId: number | undefined = undefined;
  description = '';
  documentSelectionne: any = null;

  readonly totalDocuments = computed(() => this.documents().length);
  readonly totalTaille = computed(() => {
    const total = this.documents().reduce((s, d) => s + (d.taille_octets || 0), 0);
    return this.formatTaille(total);
  });

  typeOptions = [
    { label: 'Acte', value: 'acte', icon: 'pi pi-file-edit', color: '#4f46e5' },
    { label: 'Jugement', value: 'jugement', icon: 'pi pi-balance-scale', color: '#7c3aed' },
    { label: 'Courrier', value: 'courrier', icon: 'pi pi-envelope', color: '#0ea5e9' },
    { label: 'Facture', value: 'facture', icon: 'pi pi-receipt', color: '#10b981' },
    { label: 'Pièce jointe', value: 'piece_jointe', icon: 'pi pi-paperclip', color: '#f97316' },
    { label: 'Autre', value: 'autre', icon: 'pi pi-file', color: '#64748b' }
  ];

  private apiUrl = `${environment.apiUrl}/documents`;

  constructor(
    private http: HttpClient,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadDocuments();
    this.loadDossiers();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  loadDocuments(): void {
    this.http.get<any>(this.apiUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.documents.set(data.documents || []),
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur chargement documents' })
    });
  }

  loadDossiers(): void {
    this.http.get<any>(`${environment.apiUrl}/dossiers`, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.dossiers = (data.dossiers || []).map((d: any) => ({ id: d.id, numero: d.numero_dossier, objet: d.objet })),
      error: () => {}
    });
  }

  openNew(): void {
    this.selectedFile = null;
    this.typeDocument = 'acte';
    this.description = '';
    this.dossierId = undefined;
    this.documentDialog = true;
    this.submitted = false;
  }

  voirDetails(document: any): void {
    this.documentSelectionne = document;
    this.detailsDialog = true;
  }

  editDocument(document: any): void {
    this.typeDocument = document.type_document;
    this.dossierId = document.id_dossier;
    this.description = document.description || '';
    this.selectedFile = null;
    this.documentDialog = true;
    this.submitted = false;
  }

  hideDialog(): void {
    this.documentDialog = false;
    this.submitted = false;
  }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  saveDocument(): void {
    this.submitted = true;
    if (!this.selectedFile) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Veuillez sélectionner un fichier' });
      return;
    }
    if (!this.dossierId) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Veuillez sélectionner un dossier' });
      return;
    }
    const formData = new FormData();
    formData.append('file', this.selectedFile);
    formData.append('id_dossier', this.dossierId.toString());
    formData.append('type_document', this.typeDocument);
    formData.append('description', this.description);
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
    this.http.post<any>(`${this.apiUrl}/upload`, formData, { headers }).subscribe({
      next: () => {
        this.loadDocuments();
        this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Document uploadé avec succès' });
        this.hideDialog();
      },
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
    });
  }

  deleteDocument(document: any): void {
    this.confirmationService.confirm({
      message: `Supprimer le document "${document.nom_original}" ?`,
      header: 'Confirmation',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        this.http.delete(`${this.apiUrl}/${document.id}`, { headers: this.getHeaders() }).subscribe({
          next: () => {
            this.loadDocuments();
            this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Document supprimé' });
          },
          error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
        });
      }
    });
  }

  telechargerDocument(document: any): void {
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
    this.http.get(`${this.apiUrl}/${document.id}/download`, { headers, responseType: 'blob' }).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = window.document.createElement('a');
        a.href = url;
        a.download = document.nom_original;
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur téléchargement' })
    });
  }

  getDossierLabel(id: number): string {
    const d = this.dossiers.find(x => x.id === id);
    return d ? `${d.numero} — ${d.objet}` : `#${id}`;
  }

  getTypeInfo(type: string): any {
    return this.typeOptions.find(t => t.value === type) || this.typeOptions[5];
  }

  getTypeLabel(type: string): string {
    return this.getTypeInfo(type)?.label || type;
  }

  getTypeSeverity(type: string): string {
    switch (type) {
      case 'acte': return 'info';
      case 'jugement': return 'warning';
      case 'courrier': return 'secondary';
      case 'facture': return 'success';
      case 'piece_jointe': return 'danger';
      default: return 'secondary';
    }
  }

  getMimeIcon(mime: string): string {
    if (!mime) return 'pi pi-file';
    if (mime.includes('pdf')) return 'pi pi-file-pdf';
    if (mime.includes('image')) return 'pi pi-image';
    if (mime.includes('word')) return 'pi pi-file-word';
    if (mime.includes('excel') || mime.includes('spreadsheet')) return 'pi pi-file-excel';
    return 'pi pi-file';
  }

  getMimeColor(mime: string): string {
    if (!mime) return '#64748b';
    if (mime.includes('pdf')) return '#ef4444';
    if (mime.includes('image')) return '#10b981';
    if (mime.includes('word')) return '#3b82f6';
    if (mime.includes('excel') || mime.includes('spreadsheet')) return '#16a34a';
    return '#64748b';
  }

  formatTaille(octets: number): string {
    if (!octets) return '0 B';
    for (const u of ['B', 'KB', 'MB', 'GB']) {
      if (octets < 1024) return `${octets.toFixed(1)} ${u}`;
      octets /= 1024;
    }
    return `${octets.toFixed(1)} GB`;
  }

  exportListePDF(): void {
    this.pdfService.exportDocuments(this.documents());
  }

  exportFicheDocumentPDF(): void {
    if (this.documentSelectionne) {
      this.pdfService.exportFicheDocument(
        this.documentSelectionne,
        this.getDossierLabel(this.documentSelectionne.id_dossier)
      );
    }
  }
  // ===== SELECTION MULTIPLE =====
  selectedDocuments: any[] = [];

  toggleSelectAll(items: any[]): void {
    if (this.selectedDocuments.length === items.length) {
      this.selectedDocuments = [];
    } else {
      this.selectedDocuments = [...items];
    }
  }

  toggleSelect(item: any): void {
    const i = this.selectedDocuments.findIndex((x: any) => x.id === item.id);
    if (i >= 0) { this.selectedDocuments.splice(i, 1); }
    else { this.selectedDocuments.push(item); }
  }

  isSelected(item: any): boolean {
    return this.selectedDocuments.some((x: any) => x.id === item.id);
  }

  exportSelectionPDF(): void {
    if (this.selectedDocuments.length === 0) return;
    this.pdfService.exportDocuments(this.selectedDocuments);
  }

  deleteSelectedDocuments(): void {
    if (this.selectedDocuments.length === 0) return;
    this.confirmationService.confirm({
      message: `Supprimer ${this.selectedDocuments.length} element(s) selectionne(s) ?`,
      header: 'Confirmation', icon: 'pi pi-trash',
      accept: () => {
        const ids = this.selectedDocuments.map((x: any) => x.id);
        let done = 0;
        ids.forEach((id: any) => {
          this.http.delete(`${this.apiUrl}/${id}`, { headers: this.getHeaders() }).subscribe({
            next: () => {
              done++;
              if (done === ids.length) {
                this.messageService.add({ severity: 'success', summary: 'Supprime', detail: `${ids.length} element(s) supprimes` });
                this.selectedDocuments = [];
                this.loadDocuments();
              }
            }
          });
        });
      }
    });
  }
}
