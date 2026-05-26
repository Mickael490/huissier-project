import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { InputTextModule } from 'primeng/inputtext';
import { TagModule } from 'primeng/tag';
import { DialogModule } from 'primeng/dialog';
import { MessageService } from 'primeng/api';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { PdfService } from 'src/services/pdf.service';

@Component({
  selector: 'app-audit',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    ToastModule, InputTextModule, TagModule, DialogModule
  ],
  templateUrl: './audit.component.html',
  providers: [MessageService]
})
export class AuditComponent implements OnInit {
  logs = signal<any[]>([]);
  detailsDialog = false;
  logSelectionne: any = null;
  private apiUrl = `${environment.apiUrl}/audit_logs`;

  readonly totalLogs = computed(() => this.logs().length);
  readonly totalCreations = computed(() => this.logs().filter(l => l.action === 'CREATE').length);
  readonly totalModifications = computed(() => this.logs().filter(l => l.action === 'UPDATE').length);
  readonly totalSuppressions = computed(() => this.logs().filter(l => l.action === 'DELETE').length);

  constructor(
    private http: HttpClient,
    private messageService: MessageService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadLogs();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  loadLogs(): void {
    this.http.get<any[]>(`${this.apiUrl}/`, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.logs.set(data),
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
    });
  }

  voirDetails(log: any): void {
    this.logSelectionne = log;
    this.detailsDialog = true;
  }

  getActionSeverity(action: string): string {
    switch (action) {
      case 'CREATE': return 'success';
      case 'UPDATE': return 'warning';
      case 'DELETE': return 'danger';
      case 'LOGIN': return 'info';
      case 'LOGOUT': return 'secondary';
      default: return 'secondary';
    }
  }

  getActionLabel(action: string): string {
    switch (action) {
      case 'CREATE': return 'Creation';
      case 'UPDATE': return 'Modification';
      case 'DELETE': return 'Suppression';
      case 'LOGIN': return 'Connexion';
      case 'LOGOUT': return 'Deconnexion';
      default: return action;
    }
  }

  getActionIcon(action: string): string {
    switch (action) {
      case 'CREATE': return 'pi pi-plus-circle';
      case 'UPDATE': return 'pi pi-pencil';
      case 'DELETE': return 'pi pi-trash';
      case 'LOGIN': return 'pi pi-sign-in';
      case 'LOGOUT': return 'pi pi-sign-out';
      default: return 'pi pi-info-circle';
    }
  }

  getActionColor(action: string): string {
    switch (action) {
      case 'CREATE': return '#10b981';
      case 'UPDATE': return '#f97316';
      case 'DELETE': return '#ef4444';
      case 'LOGIN': return '#3b82f6';
      case 'LOGOUT': return '#64748b';
      default: return '#94a3b8';
    }
  }

  formatDetails(details: any): string {
    if (!details) return '—';
    if (typeof details === 'string') return details;
    return JSON.stringify(details, null, 2);
  }

  exportListePDF(): void {
    this.pdfService.exportAuditLogs(this.logs());
  }

  onGlobalFilter(table: any, event: Event): void {
    table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
  }
}
