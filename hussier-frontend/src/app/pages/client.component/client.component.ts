import { Component, OnInit, signal, ViewChild, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Table, TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { ToastModule } from 'primeng/toast';
import { ToolbarModule } from 'primeng/toolbar';
import { InputTextModule } from 'primeng/inputtext';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { TagModule } from 'primeng/tag';
import { TooltipModule } from 'primeng/tooltip';
import { MessageService, ConfirmationService } from 'primeng/api';
import { ClientService } from 'src/services/clients/ClientService';
import { Client, ClientCreate, ClientUpdate, TypeClient } from 'src/types/client';
import { PdfService } from 'src/services/pdf.service';
import { environment } from 'src/environments/environment';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-client',
  standalone: true,
  imports: [
    CommonModule, FormsModule, TableModule, ButtonModule,
    DialogModule, ToastModule, ToolbarModule, InputTextModule,
    ConfirmDialogModule, TagModule, TooltipModule
  ],
  templateUrl: './client.component.html',
  providers: [MessageService, ConfirmationService]
})
export class ClientComponent implements OnInit {

  clients = signal<Client[]>([]);
  readonly nbTotal = computed(() => this.clients().length);
  readonly nbParticulier = computed(() => this.clients().filter(c => c.type_client === "particulier").length);
  readonly nbEntreprise = computed(() => this.clients().filter(c => c.type_client === "entreprise" || c.type_client === "avocat" || c.type_client === "juridiction").length);

  selectedClients: Client[] = [];
  client: Partial<Client> = {};
  clientDialog = false;
  detailsDialog = false;
  submitted = false;
  isEditMode = false;
  clientSelectionne: Client | null = null;
  TypeClient = TypeClient;

  @ViewChild('dt') dt!: Table;

  typeOptions = [
    { label: 'Particulier', value: TypeClient.PARTICULIER },
    { label: 'Avocat', value: TypeClient.AVOCAT },
    { label: 'Entreprise', value: TypeClient.ENTREPRISE },
    { label: 'Juridiction', value: TypeClient.JURIDICTION }
  ];

  constructor(
    private clientService: ClientService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService,
    private pdfService: PdfService
  ) {}

  ngOnInit(): void {
    this.loadClients();
  }

  loadClients(): void {
    this.clientService.getClients().subscribe({
      next: (data) => this.clients.set(data),
      error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur chargement clients' })
    });
  }

  openNew(): void {
    this.client = { type_client: TypeClient.PARTICULIER, cabinet_id: 1 };
    this.protegerParMotDePasse = false;
    this.isEditMode = false;
    this.clientDialog = true;
    this.submitted = false;
  }

  editClient(client: Client): void {
    this.client = { ...client };
    this.protegerParMotDePasse = !!(client as any).mot_de_passe;
    this.isEditMode = true;
    this.clientDialog = true;
  }

  dossiersDuClient: any[] = [];
  protegerParMotDePasse = false;
  motDePasseDialog = false;
  motDePasseSaisi = '';
  clientEnAttente: any = null;
  clientsDeverrouilles = new Set<number>();

voirDetails(client: Client): void {
    const c = client as any;
    if (c.mot_de_passe && !this.clientsDeverrouilles.has(client.id!)) {
      this.clientEnAttente = client;
      this.motDePasseSaisi = '';
      this.motDePasseDialog = true;
    } else {
      this.clientSelectionne = client;
      this.detailsDialog = true;
      this.chargerDossiersDuClient(client.id);
    }
  }

  verifierMotDePasse(): void {
    const c = this.clientEnAttente as any;
    if (this.motDePasseSaisi === c.mot_de_passe) {
      this.clientsDeverrouilles.add(this.clientEnAttente.id);
      this.clientSelectionne = this.clientEnAttente;
      this.motDePasseDialog = false;
      this.detailsDialog = true;
      this.chargerDossiersDuClient(this.clientEnAttente.id);
      this.motDePasseSaisi = '';
    } else {
      this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Mot de passe incorrect' });
      this.motDePasseSaisi = '';
    }
  }



getNombreDossiers(clientId: number): number {
    return this.dossiersDuClient.length;
}

getDossiersActifs(clientId: number): number {
    return this.dossiersDuClient.filter(d => d.statut === 'en_cours' || d.statut === 'nouveau').length;
}

getDossiersTermines(clientId: number): number {
    return this.dossiersDuClient.filter(d => d.statut === 'termine').length;
}

  editFromDetails(): void {
    this.detailsDialog = false;
    if (this.clientSelectionne) {
      this.editClient(this.clientSelectionne);
    }
  }

  exportClientPDF(): void {
    if (this.clientSelectionne) {
        this.pdfService.exportFicheClient(
            this.clientSelectionne,
            this.dossiersDuClient,
            this.paiementsDuClient
        );
    }
}

  

  hideDialog(): void {
    this.clientDialog = false;
    this.submitted = false;
  }

  saveClient(): void {
    this.submitted = true;
    if (!this.protegerParMotDePasse) {
      (this.client as any).mot_de_passe = null;
    }
    if (!this.client.nom || !this.client.type_client) {
      this.messageService.add({ severity: 'warn', summary: 'Attention', detail: 'Veuillez remplir les champs obligatoires' });
      return;
    }
    if (this.isEditMode && this.client.id) {
      this.clientService.updateClient(this.client.id, this.client as ClientUpdate).subscribe({
        next: () => {
          this.loadClients();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Client mis à jour' });
          this.hideDialog();
        },
        error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur mise à jour' })
      });
    } else {
      this.clientService.createClient(this.client as ClientCreate).subscribe({
        next: () => {
          this.loadClients();
          this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Client créé' });
          this.hideDialog();
        },
        error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur création' })
      });
    }
  }

  deleteClient(client: Client): void {
    this.confirmationService.confirm({
      message: `Voulez-vous vraiment supprimer le client ${client.nom} ${client.prenom || ''} ?`,
      header: 'Confirmation de suppression',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        this.clientService.deleteClient(client.id).subscribe({
          next: () => {
            this.loadClients();
            this.messageService.add({ severity: 'success', summary: 'Succès', detail: 'Client supprimé' });
          },
          error: () => this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Erreur suppression' })
        });
      }
    });
  }

  onGlobalFilter(table: Table, event: Event): void {
    table.filterGlobal((event.target as HTMLInputElement).value, 'contains');
  }

  getInitiales(client: Client): string {
    if (client.type_client === TypeClient.ENTREPRISE || client.type_client === TypeClient.JURIDICTION) {
      return client.nom?.charAt(0)?.toUpperCase() || 'E';
    }
    const nom = client.nom?.charAt(0) || '';
    const prenom = client.prenom?.charAt(0) || '';
    return (nom + prenom).toUpperCase() || '?';
  }

  getAvatarColor(type: string): string {
    switch (type) {
      case 'particulier': return 'linear-gradient(135deg, #1e3a5f, #2d6a9f)';
      case 'entreprise': return 'linear-gradient(135deg, #065f46, #059669)';
      case 'avocat': return 'linear-gradient(135deg, #92400e, #d97706)';
      case 'juridiction': return 'linear-gradient(135deg, #6b21a8, #9333ea)';
      default: return 'linear-gradient(135deg, #1e3a5f, #2d6a9f)';
    }
  }

  getTypeSeverity(type: string): string {
    switch (type) {
      case 'particulier': return 'info';
      case 'entreprise': return 'success';
      case 'avocat': return 'warning';
      case 'juridiction': return 'danger';
      default: return 'info';
    }
  }

  getTypeLabel(type: string): string {
    switch (type) {
      case 'particulier': return 'Particulier';
      case 'entreprise': return 'Entreprise';
      case 'avocat': return 'Avocat';
      case 'juridiction': return 'Juridiction';
      default: return type;
    }
  }

  getNomAffiche(client: Client): string {
    if (client.type_client === TypeClient.ENTREPRISE || client.type_client === TypeClient.JURIDICTION) {
      return client.nom;
    }
    return `${client.nom} ${client.prenom || ''}`.trim();
  }

  isPersonneMorale(type?: string): boolean {
    return type === TypeClient.ENTREPRISE || type === TypeClient.JURIDICTION;
  }

  
  exportPDF(): void {
    this.pdfService.exportClients(this.clients());
  }

  exportSelectionPDF(): void {
    if (!this.selectedClients.length) return;
    this.pdfService.exportClients(this.selectedClients);
  }

  deleteSelectedClients(): void {
    if (!this.selectedClients.length) return;
    this.confirmationService.confirm({
      message: `Supprimer les ${this.selectedClients.length} client(s) sélectionné(s) ?`,
      header: 'Confirmation de suppression',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        const calls = this.selectedClients.filter(c => c.id != null).map(c => this.clientService.deleteClient(c.id));
        if (!calls.length) return;
        forkJoin(calls).subscribe({
          next: () => {
            const n = calls.length;
            this.selectedClients = [];
            this.loadClients();
            this.messageService.add({ severity: 'success', summary: 'Supprimé', detail: `${n} client(s) supprimé(s)` });
          },
          error: () => {
            this.messageService.add({ severity: 'error', summary: 'Erreur', detail: 'Suppression partielle impossible' });
            this.loadClients();
          }
        });
      }
    });
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

paiementsDuClient: any[] = [];

chargerDossiersDuClient(clientId: number): void {
    const token = localStorage.getItem('token');
    const headers = { 'Authorization': `Bearer ${token}` };
    
    // Charger les dossiers
    fetch(`${environment.apiUrl}/dossiers?client_id=${clientId}`, { headers })
        .then(r => r.json())
        .then(data => {
            this.dossiersDuClient = data.dossiers || [];
            // Charger les paiements pour chaque dossier
            this.paiementsDuClient = [];
            this.dossiersDuClient.forEach(dos => {
                fetch(`${environment.apiUrl}/paiements?id_dossier=${dos.id}`, { headers })
                    .then(r => r.json())
                    .then(paiements => {
                        if (Array.isArray(paiements)) {
                            this.paiementsDuClient = [...this.paiementsDuClient, ...paiements];
                        }
                    });
            });
        });
}

getTotalPaiements(): number {
    return this.paiementsDuClient.reduce((sum, p) => sum + (p.montant || 0), 0);
}

getNombrePaiements(): number {
    return this.paiementsDuClient.length;
}

getMontantMoyen(): number {
    if (this.paiementsDuClient.length === 0) return 0;
    return this.getTotalPaiements() / this.paiementsDuClient.length;
}

}