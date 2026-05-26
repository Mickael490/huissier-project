import { Component, OnInit, signal, computed } from '@angular/core';
import { TooltipModule } from 'primeng/tooltip';
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
import { UtilisateurService } from 'src/services/utilisateurs/UtilisateurService';
import { Utilisateur, UtilisateurCreate, UtilisateurUpdate, RoleEnum } from 'src/types/utilisateur';
import { PdfService } from 'src/services/pdf.service';

@Component({
  selector: 'app-utilisateur',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    DialogModule, ToastModule, InputTextModule,
    ConfirmDialogModule, TagModule, TooltipModule, TextareaModule
  ],
  templateUrl: './utilisateur.component.html',
  providers: [MessageService, ConfirmationService]
})
export class UtilisateurComponent implements OnInit {
  utilisateurs = signal<Utilisateur[]>([]);
  utilisateur: Partial<Utilisateur> & { mot_de_passe?: string } = {};
  utilisateurDialog = false;
  detailsDialog = false;
  submitted = false;
  isEditMode = false;
  utilisateurSelectionne: any = null;

  readonly totalUtilisateurs = computed(() => this.utilisateurs().length);
  readonly totalActifs = computed(() => this.utilisateurs().filter(u => u.actif).length);
  readonly totalAdmins = computed(() => this.utilisateurs().filter(u => u.role === RoleEnum.ADMIN).length);

  roleOptions = [
    { label: 'Administrateur', value: RoleEnum.ADMIN, color: '#ef4444', icon: 'pi pi-shield' },
    { label: 'Huissier', value: RoleEnum.HUISSIER, color: '#4f46e5', icon: 'pi pi-star' },
    { label: 'Clerc', value: RoleEnum.CLERC, color: '#0ea5e9', icon: 'pi pi-briefcase' },
    { label: 'Assistant', value: RoleEnum.ASSISTANT, color: '#10b981', icon: 'pi pi-user' },
    { label: 'Secretaire', value: RoleEnum.SECRETAIRE, color: '#f97316', icon: 'pi pi-inbox' }
  ];

  constructor(
    private utilisateurService: UtilisateurService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadUtilisateurs();
  }

  loadUtilisateurs(): void {
    this.utilisateurService.getUtilisateurs().subscribe({
      next: (data) => this.utilisateurs.set(data),
      error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur chargement utilisateurs' })
    });
  }

  openNew(): void {
    this.utilisateur = { role: RoleEnum.SECRETAIRE, actif: true };
    this.isEditMode = false;
    this.utilisateurDialog = true;
    this.submitted = false;
  }

  editUtilisateur(utilisateur: Utilisateur): void {
    this.utilisateur = { ...utilisateur };
    this.isEditMode = true;
    this.utilisateurDialog = true;
  }

  voirDetails(utilisateur: any): void {
    this.utilisateurSelectionne = utilisateur;
    this.detailsDialog = true;
  }

  editFromDetails(): void {
    this.detailsDialog = false;
    this.editUtilisateur(this.utilisateurSelectionne);
  }

  hideDialog(): void {
    this.utilisateurDialog = false;
    this.submitted = false;
  }

  saveUtilisateur(): void {
    this.submitted = true;
    if (!this.utilisateur.nom || !this.utilisateur.email || !this.utilisateur.role) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Veuillez remplir les champs obligatoires' });
      return;
    }
    if (this.isEditMode && this.utilisateur.id) {
      const updateData: UtilisateurUpdate = {
        nom: this.utilisateur.nom,
        prenom: this.utilisateur.prenom || '',
        email: this.utilisateur.email,
        telephone: this.utilisateur.telephone,
        role: this.utilisateur.role,
        actif: this.utilisateur.actif
      };
      this.utilisateurService.updateUtilisateur(this.utilisateur.id, updateData).subscribe({
        next: () => {
          this.loadUtilisateurs();
          this.messageService.add({ severity: 'success', summary: 'Succes', detail: 'Utilisateur mis a jour' });
          this.hideDialog();
        },
        error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur mise a jour' })
      });
    } else {
      if (!this.utilisateur.mot_de_passe) {
        this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Le mot de passe est obligatoire' });
        return;
      }
      const createData: UtilisateurCreate = {
        nom: this.utilisateur.nom!,
        prenom: this.utilisateur.prenom || '',
        email: this.utilisateur.email!,
        telephone: this.utilisateur.telephone,
        role: this.utilisateur.role!,
        mot_de_passe: this.utilisateur.mot_de_passe,
        id_cabinet: 1,
        actif: this.utilisateur.actif ?? true
      };
      this.utilisateurService.createUtilisateur(createData).subscribe({
        next: () => {
          this.loadUtilisateurs();
          this.messageService.add({ severity: 'success', summary: 'Succes', detail: 'Utilisateur cree' });
          this.hideDialog();
        },
        error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur creation' })
      });
    }
  }

  deleteUtilisateur(utilisateur: Utilisateur): void {
    this.confirmationService.confirm({
      message: `Supprimer l'utilisateur ${utilisateur.nom} ?`,
      header: 'Confirmation',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        this.utilisateurService.deleteUtilisateur(utilisateur.id!).subscribe({
          next: () => {
            this.loadUtilisateurs();
            this.messageService.add({ severity: 'success', summary: 'Succes', detail: 'Utilisateur supprime' });
          },
          error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur suppression' })
        });
      }
    });
  }

  getRoleInfo(role: string): any {
    return this.roleOptions.find(r => r.value === role) || this.roleOptions[4];
  }

  getRoleLabel(role: string): string {
    return this.getRoleInfo(role)?.label || role;
  }

  getRoleSeverity(role: string): string {
    switch (role) {
      case RoleEnum.ADMIN: return 'danger';
      case RoleEnum.HUISSIER: return 'info';
      case RoleEnum.CLERC: return 'warning';
      case RoleEnum.ASSISTANT: return 'success';
      default: return 'secondary';
    }
  }

  getInitiales(u: any): string {
    const nom = u.nom?.charAt(0) || '';
    const prenom = u.prenom?.charAt(0) || '';
    return (nom + prenom).toUpperCase();
  }

  exportListePDF(): void {
    this.pdfService.exportUtilisateurs(this.utilisateurs());
  }
}
