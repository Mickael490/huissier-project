import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { TagModule } from 'primeng/tag';
import { MessageService } from 'primeng/api';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-roles',
  standalone: true,
  imports: [CommonModule, FormsModule, TableModule, ButtonModule, DialogModule, ToastModule, TagModule],
  templateUrl: './roles.component.html',
  providers: [MessageService]
})
export class RolesComponent implements OnInit {
  utilisateurs = signal<any[]>([]);
  roleDialog = false;
  selectedUtilisateur: any = null;
  selectedRole: string = '';

  roles = [
    {
      value: 'ADMIN',
      label: 'Administrateur',
      icon: '👑',
      severity: 'danger',
      permissions: [
        'Accès total au système',
        'Gestion des utilisateurs et rôles',
        'Gestion du cabinet',
        'Consultation des audits',
        'Toutes les fonctionnalités'
      ]
    },
    {
      value: 'HUISSIER',
      label: 'Huissier',
      icon: '⚖️',
      severity: 'warning',
      permissions: [
        'Dossiers, Clients, Actes',
        'Paiements, Affectations',
        'Documents, Archives',
        'Agenda'
      ]
    },
    {
      value: 'CLERC',
      label: 'Clerc',
      icon: '📋',
      severity: 'info',
      permissions: [
        'Dossiers, Clients',
        'Actes, Documents',
        'Agenda'
      ]
    },
    {
      value: 'ASSISTANT',
      label: 'Assistant',
      icon: '🔧',
      severity: 'success',
      permissions: [
        'Dossiers',
        'Documents',
        'Agenda'
      ]
    },
    {
      value: 'SECRETAIRE',
      label: 'Secrétaire',
      icon: '📝',
      severity: 'secondary',
      permissions: [
        'Clients',
        'Agenda uniquement'
      ]
    }
  ];

  constructor(
    private http: HttpClient,
    private messageService: MessageService
  ) {}

  ngOnInit(): void {
    this.loadUtilisateurs();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  loadUtilisateurs(): void {
    this.http.get<any[]>(`${environment.apiUrl}/utilisateurs`, { headers: this.getHeaders() }).subscribe({
      next: (data) => this.utilisateurs.set(data),
      error: () => {}
    });
  }

  getRoleInfo(role: string) {
    return this.roles.find(r => r.value === role) || this.roles[4];
  }

  ouvrirGestionRole(utilisateur: any): void {
    this.selectedUtilisateur = utilisateur;
    this.selectedRole = utilisateur.role;
    this.roleDialog = true;
  }

  saveRole(): void {
    if (!this.selectedUtilisateur || !this.selectedRole) return;
    this.http.put(
      `${environment.apiUrl}/utilisateurs/${this.selectedUtilisateur.id}`,
      { role: this.selectedRole },
      { headers: this.getHeaders() }
    ).subscribe({
      next: () => {
        this.loadUtilisateurs();
        this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Rôle mis à jour avec succès' });
        this.roleDialog = false;
      },
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
    });
  }

  getRoleSeverity(role: string): any {
    return this.getRoleInfo(role)?.severity || 'secondary';
  }
}