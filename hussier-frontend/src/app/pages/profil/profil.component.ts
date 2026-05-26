import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { ToastModule } from 'primeng/toast';
import { TagModule } from 'primeng/tag';
import { MessageService } from 'primeng/api';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-profil',
  standalone: true,
  imports: [CommonModule, FormsModule, ButtonModule, InputTextModule, ToastModule, TagModule],
  templateUrl: './profil.component.html',
  providers: [MessageService]
})
export class ProfilComponent implements OnInit {
  utilisateur: any = {};
  ancienMotDePasse: string = '';
  nouveauMotDePasse: string = '';
  confirmMotDePasse: string = '';
  private apiUrl = `${environment.apiUrl}/utilisateurs`;

  constructor(
    private http: HttpClient,
    private messageService: MessageService
  ) {}

  ngOnInit(): void {
    this.loadProfil();
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  loadProfil(): void {
    this.utilisateur = {
      nom: localStorage.getItem('nom') || '',
      prenom: localStorage.getItem('prenom') || '',
      role: localStorage.getItem('role') || '',
      email: ''
    };
    this.http.get<any[]>(this.apiUrl, { headers: this.getHeaders() }).subscribe({
      next: (data) => {
        const email = data.find(u => u.nom === this.utilisateur.nom);
        if (email) this.utilisateur = { ...this.utilisateur, ...email };
      },
      error: () => {}
    });
  }

  getRoleSeverity(role: string): string {
    switch (role) {
      case 'admin': return 'danger';
      case 'huissier': return 'warning';
      case 'clerc': return 'info';
      case 'assistant': return 'success';
      default: return 'secondary';
    }
  }

  updateProfil(): void {
    if (!this.utilisateur.id) return;
    this.http.put(`${this.apiUrl}/${this.utilisateur.id}`, {
      nom: this.utilisateur.nom,
      prenom: this.utilisateur.prenom,
      telephone: this.utilisateur.telephone
    }, { headers: this.getHeaders() }).subscribe({
      next: () => {
        localStorage.setItem('nom', this.utilisateur.nom);
        localStorage.setItem('prenom', this.utilisateur.prenom);
        this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Profil mis à jour' });
      },
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
    });
  }

  updateMotDePasse(): void {
    if (this.nouveauMotDePasse !== this.confirmMotDePasse) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Les mots de passe ne correspondent pas' });
      return;
    }
    if (this.nouveauMotDePasse.length < 8) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Le mot de passe doit avoir au moins 8 caractères' });
      return;
    }
    if (!this.utilisateur.id) return;
    this.http.put(`${this.apiUrl}/${this.utilisateur.id}`, {
      mot_de_passe: this.nouveauMotDePasse
    }, { headers: this.getHeaders() }).subscribe({
      next: () => {
        this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Mot de passe mis à jour' });
        this.ancienMotDePasse = '';
        this.nouveauMotDePasse = '';
        this.confirmMotDePasse = '';
      },
      error: (err) => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: JSON.stringify(err.error) })
    });
  }
}