import { Component, OnInit, signal, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Table, TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { ToolbarModule } from 'primeng/toolbar';
import { InputTextModule } from 'primeng/inputtext';
import { TextareaModule } from 'primeng/textarea';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { TagModule } from 'primeng/tag';
import { MessageService, ConfirmationService } from 'primeng/api';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { PdfService } from 'src/services/pdf.service';
import { ExcelService } from 'src/services/excel.service';

@Component({
  selector: 'app-acte',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    DialogModule, ToastModule, ToolbarModule, InputTextModule,
    TextareaModule, ConfirmDialogModule, TagModule
  ],
  templateUrl: './acte.component.html',
  providers: [MessageService, ConfirmationService]
})
export class ActeComponent implements OnInit {

  actes = signal<any[]>([]);
  dossiers: { id: number; numero: string; objet: string }[] = [];
  acte: any = {};
  acteDialog = false;
  detailsDialog = false;
  submitted = false;
  isEditMode = false;
  acteSelectionne: any = null;

  @ViewChild('dt') dt!: Table;

  private apiUrl = `${environment.apiUrl}/actes`;
  private dossierUrl = `${environment.apiUrl}/dossiers`;

  typeOptions = [
    { label: 'Signification', value: 'signification', icon: 'pi pi-send', color: '#4f46e5' },
    { label: 'Constat', value: 'constat', icon: 'pi pi-eye', color: '#0ea5e9' },
    { label: 'Saisie', value: 'saisie', icon: 'pi pi-lock', color: '#ef4444' },
    { label: 'Recouvrement', value: 'recouvrement', icon: 'pi pi-dollar', color: '#10b981' },
    { label: 'Expulsion', value: 'expulsion', icon: 'pi pi-home', color: '#f97316' },
    { label: 'Commandement', value: 'commandement', icon: 'pi pi-megaphone', color: '#8b5cf6' },
    { label: 'Proces verbal', value: 'proces_verbal', icon: 'pi pi-file-edit', color: '#06b6d4' },
    { label: 'Inventaire', value: 'inventaire', icon: 'pi pi-list', color: '#64748b' },
    { label: 'Autre', value: 'autre', icon: 'pi pi-file', color: '#94a3b8' }
  ];

  constructor(
    private http: HttpClient,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService,
    public excelService: ExcelService
  ) {}

  ngOnInit(): void {
    this.loadActes();
    this.loadDossiers();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
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

  loadActes(): void {
    this.http.get<any[]>(this.apiUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.actes.set(data),
      error: () => this.messageService.add({
        severity: 'error', summary: 'Erreur', detail: 'Erreur lors du chargement des actes'
      })
    });
  }

  openNew(): void {
    this.acte = {
      type_acte: 'signification',
      date_acte: new Date().toISOString().split('T')[0]
    };
    this.isEditMode = false;
    this.acteDialog = true;
    this.submitted = false;
  }

  editActe(acte: any): void {
    this.acte = { ...acte };
    if (this.acte.date_acte) {
      this.acte.date_acte = this.acte.date_acte.split('T')[0];
    }
    this.isEditMode = true;
    this.acteDialog = true;
  }

  voirDetails(acte: any): void {
    this.acteSelectionne = acte;
    this.detailsDialog = true;
  }

  editFromDetails(): void {
    this.detailsDialog = false;
    this.editActe(this.acteSelectionne);
  }

  hideDialog(): void {
    this.acteDialog = false;
    this.submitted = false;
  }

  saveActe(): void {
    // Convertir type_acte en minuscule
    this.acte.type_acte = this.acte.type_acte.toLowerCase();
    this.submitted = true;
    if (!this.acte.id_dossier || !this.acte.type_acte || !this.acte.date_acte) {
      this.messageService.add({
        severity: 'warn', summary: 'Attention', detail: 'Veuillez remplir les champs obligatoires'
      });
      return;
    }
    if (this.isEditMode && this.acte.id) {
      this.http.put(`${this.apiUrl}/${this.acte.id}`, this.acte, { headers: this.getHeaders() }).subscribe({
        next: () => {
          this.loadActes();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Acte mis à jour' });
          this.hideDialog();
        },
        error: (err) => this.messageService.add({
          severity: 'error', summary: 'Erreur', detail: err.error?.detail || 'Erreur mise à jour'
        })
      });
    } else {
      this.http.post(this.apiUrl, this.acte, { headers: this.getHeaders() }).subscribe({
        next: () => {
          this.loadActes();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Acte créé' });
          this.hideDialog();
        },
        error: (err) => this.messageService.add({
          severity: 'error', summary: 'Erreur', detail: err.error?.detail || 'Erreur création'
        })
      });
    }
  }

  deleteActe(acte: any): void {
    this.confirmationService.confirm({
      message: `Voulez-vous vraiment supprimer cet acte ?`,
      header: 'Confirmation de suppression',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        this.http.delete(`${this.apiUrl}/${acte.id}`, { headers: this.getHeaders() }).subscribe({
          next: () => {
            this.loadActes();
            this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Acte supprimé' });
          },
          error: (err) => this.messageService.add({
            severity: 'error', summary: 'Erreur', detail: err.error?.detail || 'Erreur suppression'
          })
        });
      }
    });
  }

  onGlobalFilter(table: Table, event: Event): void {
    table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
  }

  // ✅ Méthodes de comptage pour les stats
  countByType(type: string): number {
    return this.actes().filter(a => a.type_acte === type).length;
  }

  getDossierNumero(id: number): string {
    const d = this.dossiers.find(x => x.id === id);
    return d ? d.numero : `#${id}`;
  }

  getDossierObjet(id: number): string {
    const d = this.dossiers.find(x => x.id === id);
    return d ? d.objet : '';
  }

  getTypeOption(type: string) {
    return this.typeOptions.find(t => t.value === type) || this.typeOptions[this.typeOptions.length - 1];
  }

  getTypeLabel(type: string): string {
    return this.getTypeOption(type)?.label || type;
  }

  getTypeIcon(type: string): string {
    return this.getTypeOption(type)?.icon || 'pi pi-file';
  }

  getTypeColor(type: string): string {
    const colors: { [key: string]: string } = {
      signification: 'linear-gradient(135deg, #1e3a5f, #2d6a9f)',
      constat: 'linear-gradient(135deg, #92400e, #d97706)',
      saisie: 'linear-gradient(135deg, #7f1d1d, #ef4444)',
      recouvrement: 'linear-gradient(135deg, #065f46, #059669)',
      expulsion: 'linear-gradient(135deg, #4c1d95, #7c3aed)',
      commandement: 'linear-gradient(135deg, #991b1b, #dc2626)',
      proces_verbal: 'linear-gradient(135deg, #0e7490, #0891b2)',
      inventaire: 'linear-gradient(135deg, #3f6212, #65a30d)',
      autre: 'linear-gradient(135deg, #334155, #64748b)',
    };
    return colors[type] || colors['autre'];
  }

  getTypeSeverity(type: string): string {
    const severities: { [key: string]: string } = {
      signification: 'info',
      constat: 'warning',
      saisie: 'danger',
      recouvrement: 'success',
      expulsion: 'danger',
      commandement: 'danger',
      proces_verbal: 'info',
      inventaire: 'success',
      autre: 'secondary',
    };
    return severities[type] || 'secondary';
  }

  exportActePDF(acte: any): void {
    const num = this.getDossierNumero(acte.id_dossier);
    const obj = this.getDossierObjet(acte.id_dossier);
    this.pdfService.exportActeDetails(acte, num, obj);
  }

  exportPDF(): void {
    this.pdfService.exportActes(this.actes());
  }
  // ===== SELECTION MULTIPLE =====
  selectedActes: any[] = [];

  toggleSelectAll(items: any[]): void {
    if (this.selectedActes.length === items.length) {
      this.selectedActes = [];
    } else {
      this.selectedActes = [...items];
    }
  }

  toggleSelect(item: any): void {
    const i = this.selectedActes.findIndex((x: any) => x.id === item.id);
    if (i >= 0) { this.selectedActes.splice(i, 1); }
    else { this.selectedActes.push(item); }
  }

  isSelected(item: any): boolean {
    return this.selectedActes.some((x: any) => x.id === item.id);
  }

  exportSelectionActesPDF(): void {
    if (this.selectedActes.length === 0) return;
    this.pdfService.exportActes(this.selectedActes);
  }

  deleteSelected(): void {
    if (this.selectedActes.length === 0) return;
    this.confirmationService.confirm({
      message: `Supprimer ${this.selectedActes.length} element(s) ?`,
      header: 'Confirmation', icon: 'pi pi-trash',
      accept: () => {
        const ids = this.selectedActes.map((x: any) => x.id);
        let done = 0;
        ids.forEach((id: any) => {
          this.http.delete(`${this.apiUrl}/${id}`, { headers: this.getHeaders() }).subscribe({
            next: () => {
              done++;
              if (done === ids.length) {
                this.messageService.add({ severity: 'success', summary: 'Supprime', detail: `${ids.length} element(s) supprimes` });
                this.selectedActes = [];
                this.loadActes();
              }
            }
          });
        });
      }
    });
  }
}
