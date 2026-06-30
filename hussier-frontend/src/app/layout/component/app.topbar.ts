import { Component, OnInit, OnDestroy } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { LayoutService } from '../service/layout.service';
import { environment } from 'src/environments/environment';

@Component({
    selector: 'app-topbar',
    standalone: true,
    imports: [RouterModule, CommonModule, FormsModule],
    template: `
    <div class="layout-topbar" style="background:linear-gradient(135deg, #1e3a5f, #2d6a9f); border-bottom:1px solid rgba(255,255,255,0.08);">
        <div class="layout-topbar-logo-container">
            <button class="layout-menu-button layout-topbar-action" (click)="layoutService.onMenuToggle()"
                style="color:#e2e8f0; background:rgba(255,255,255,0.08); border:none; border-radius:8px; width:36px; height:36px; display:flex; align-items:center; justify-content:center; cursor:pointer;">
                <i class="pi pi-bars" style="font-size:16px;"></i>
            </button>
            <a class="layout-topbar-logo" routerLink="/" style="text-decoration:none; display:flex; align-items:center; gap:10px; margin-left:12px;">
                <div style="width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg, #2d6a9f, #4f46e5); display:flex; align-items:center; justify-content:center;">
                    <i class="pi pi-building" style="color:white; font-size:16px;"></i>
                </div>
                <div>
                    <div style="font-size:14px; font-weight:700; color:white; line-height:1.2;">Cabinet Me SAWADOGO</div>
                    <div style="font-size:10px; color:rgba(255,255,255,0.6); letter-spacing:1px; text-transform:uppercase;">Huissier de Justice</div>
                </div>
            </a>
        </div>

        <!-- RECHERCHE GLOBALE -->
        <div style="position:relative; flex:1; max-width:400px; margin:0 16px;">
            <i class="pi pi-search" style="position:absolute; left:12px; top:50%; transform:translateY(-50%); color:rgba(255,255,255,0.5); font-size:14px; z-index:1;"></i>
            <input type="text" [(ngModel)]="searchQuery" (input)="onSearch()" (focus)="showResults=true"
                placeholder="Rechercher dossier, client, acte..."
                style="width:100%; padding:8px 12px 8px 36px; border-radius:10px; border:1px solid rgba(255,255,255,0.15); background:rgba(255,255,255,0.1); color:white; font-size:13px; outline:none;"
                (keydown.escape)="clearSearch()" />
            <i *ngIf="searchQuery" class="pi pi-times" (click)="clearSearch()"
                style="position:absolute; right:10px; top:50%; transform:translateY(-50%); color:rgba(255,255,255,0.5); cursor:pointer; font-size:13px;"></i>

            <!-- Résultats -->
            <div *ngIf="showResults && searchQuery.length >= 2"
                style="position:absolute; top:calc(100% + 8px); left:0; right:0; background:white; border-radius:12px; box-shadow:0 8px 32px rgba(0,0,0,0.2); z-index:9999; overflow:hidden; max-height:400px; overflow-y:auto;">

                <div *ngIf="loading" style="padding:16px; text-align:center; color:#94a3b8; font-size:13px;">
                    <i class="pi pi-spin pi-spinner"></i> Recherche...
                </div>

                <div *ngIf="!loading && totalResultats === 0" style="padding:16px; text-align:center; color:#94a3b8; font-size:13px;">
                    Aucun résultat pour "{{ searchQuery }}"
                </div>

                <!-- Dossiers -->
                <div *ngIf="resultats.dossiers?.length > 0">
                    <div style="padding:8px 14px; font-size:11px; font-weight:700; color:#1e3a5f; background:#f8fafc; text-transform:uppercase; letter-spacing:1px;">
                        <i class="pi pi-folder" style="margin-right:6px;"></i>Dossiers
                    </div>
                    <div *ngFor="let d of resultats.dossiers" (click)="naviguer('/pages/dossier')"
                        style="padding:10px 14px; cursor:pointer; border-bottom:1px solid #f1f5f9; display:flex; align-items:center; gap:10px;"
                        onmouseover="this.style.background='#f5f3ff'" onmouseout="this.style.background='white'">
                        <div style="width:32px; height:32px; border-radius:8px; background:#ede9fe; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                            <i class="pi pi-folder" style="color:#4f46e5; font-size:13px;"></i>
                        </div>
                        <div>
                            <div style="font-weight:700; color:#1e293b; font-size:13px;">{{ d.numero_dossier }}</div>
                            <div style="font-size:11px; color:#94a3b8;">{{ d.objet }} · {{ d.type_dossier }}</div>
                        </div>
                        <span style="margin-left:auto; font-size:11px; padding:2px 8px; border-radius:20px; background:#ede9fe; color:#4f46e5;">{{ d.statut }}</span>
                    </div>
                </div>

                <!-- Clients -->
                <div *ngIf="resultats.clients?.length > 0">
                    <div style="padding:8px 14px; font-size:11px; font-weight:700; color:#1e3a5f; background:#f8fafc; text-transform:uppercase; letter-spacing:1px;">
                        <i class="pi pi-users" style="margin-right:6px;"></i>Clients
                    </div>
                    <div *ngFor="let c of resultats.clients" (click)="naviguer('/pages/client')"
                        style="padding:10px 14px; cursor:pointer; border-bottom:1px solid #f1f5f9; display:flex; align-items:center; gap:10px;"
                        onmouseover="this.style.background='#f0fdf4'" onmouseout="this.style.background='white'">
                        <div style="width:32px; height:32px; border-radius:50%; background:linear-gradient(135deg,#10b981,#34d399); display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:12px; flex-shrink:0;">
                            {{ (c.prenom?.charAt(0) || c.nom?.charAt(0) || '?').toUpperCase() }}
                        </div>
                        <div>
                            <div style="font-weight:700; color:#1e293b; font-size:13px;">{{ c.prenom }} {{ c.nom }}</div>
                            <div style="font-size:11px; color:#94a3b8;">{{ c.email || c.telephone }}</div>
                        </div>
                    </div>
                </div>

                <!-- Actes -->
                <div *ngIf="resultats.actes?.length > 0">
                    <div style="padding:8px 14px; font-size:11px; font-weight:700; color:#1e3a5f; background:#f8fafc; text-transform:uppercase; letter-spacing:1px;">
                        <i class="pi pi-file-edit" style="margin-right:6px;"></i>Actes
                    </div>
                    <div *ngFor="let a of resultats.actes" (click)="naviguer('/pages/acte')"
                        style="padding:10px 14px; cursor:pointer; border-bottom:1px solid #f1f5f9; display:flex; align-items:center; gap:10px;"
                        onmouseover="this.style.background='#fef3c7'" onmouseout="this.style.background='white'">
                        <div style="width:32px; height:32px; border-radius:8px; background:#fef3c7; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                            <i class="pi pi-file-edit" style="color:#f59e0b; font-size:13px;"></i>
                        </div>
                        <div>
                            <div style="font-weight:700; color:#1e293b; font-size:13px;">{{ a.type_acte }}</div>
                            <div style="font-size:11px; color:#94a3b8;">{{ a.lieu || '—' }} · {{ a.date_acte | date:"dd/MM/yyyy" }}</div>
                        </div>
                    </div>
                </div>

                <div *ngIf="!loading && totalResultats > 0" style="padding:10px 14px; text-align:center; font-size:12px; color:#94a3b8; background:#f8fafc;">
                    {{ totalResultats }} résultat(s) trouvé(s)
                </div>
            </div>
        </div>

        <div class="layout-topbar-actions" style="display:flex; align-items:center; gap:8px;">
            <div style="background:rgba(255,255,255,0.08); border-radius:8px; padding:6px 12px; display:flex; align-items:center; gap:6px;">
                <i class="pi pi-clock" style="color:#64a0c8; font-size:13px;"></i>
                <span style="color:#e2e8f0; font-size:13px; font-weight:600; font-family:monospace;">{{ heureActuelle }}</span>
            </div>
            <div style="background:rgba(255,255,255,0.08); border-radius:8px; padding:6px 12px; display:flex; align-items:center; gap:8px;">
                <div style="width:28px; height:28px; border-radius:50%; background:linear-gradient(135deg, #2d6a9f, #4f46e5); display:flex; align-items:center; justify-content:center; color:white; font-size:11px; font-weight:700;">
                    {{ initiales }}
                </div>
                <div>
                    <div style="font-size:13px; font-weight:600; color:white; line-height:1.2;">{{ nomUtilisateur }}</div>
                    <div style="font-size:10px; color:#64a0c8; text-transform:uppercase; letter-spacing:1px;">{{ roleUtilisateur }}</div>
                </div>
            </div>
            <button type="button" (click)="voirProfil()" pTooltip="Mon profil"
                style="width:36px; height:36px; border-radius:8px; background:rgba(255,255,255,0.08); border:none; color:#e2e8f0; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                <i class="pi pi-user" style="font-size:15px;"></i>
            </button>
            <button type="button" (click)="voirUtilisateurs()" pTooltip="Gestion roles"
                style="width:36px; height:36px; border-radius:8px; background:rgba(255,255,255,0.08); border:none; color:#e2e8f0; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                <i class="pi pi-shield" style="font-size:15px;"></i>
            </button>
            <button type="button" (click)="toggleDarkMode()" pTooltip="Changer theme"
                style="width:36px; height:36px; border-radius:8px; background:rgba(255,255,255,0.08); border:none; color:#e2e8f0; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                <i [class]="layoutService.isDarkTheme() ? 'pi pi-sun' : 'pi pi-moon'" style="font-size:15px;"></i>
            </button>
            <button type="button" (click)="logout()" pTooltip="Se deconnecter"
                style="width:36px; height:36px; border-radius:8px; background:rgba(239,68,68,0.2); border:1px solid rgba(239,68,68,0.3); color:#fca5a5; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                <i class="pi pi-sign-out" style="font-size:15px;"></i>
            </button>
        </div>
    </div>
    `
})
export class AppTopbar implements OnInit, OnDestroy {
    nomUtilisateur = '';
    roleUtilisateur = '';
    initiales = '';
    heureActuelle = '';
    searchQuery = '';
    showResults = false;
    loading = false;
    resultats: any = { dossiers: [], clients: [], actes: [] };
    private timer: any;
    private searchTimer: any;

    get totalResultats(): number {
        return (this.resultats.dossiers?.length || 0) +
               (this.resultats.clients?.length || 0) +
               (this.resultats.actes?.length || 0);
    }

    constructor(public layoutService: LayoutService, private router: Router, private http: HttpClient) {}

    ngOnInit() {
        const nom = localStorage.getItem('nom') || '';
        const prenom = localStorage.getItem('prenom') || '';
        this.nomUtilisateur = (prenom + ' ' + nom).trim() || 'Utilisateur';
        this.roleUtilisateur = localStorage.getItem('role') || '';
        this.initiales = ((prenom.charAt(0)) + (nom.charAt(0))).toUpperCase() || 'U';
        this.updateHeure();
        this.timer = setInterval(() => this.updateHeure(), 1000);

        document.addEventListener('click', (e: any) => {
            if (!e.target.closest('.layout-topbar')) this.showResults = false;
        });
    }

    ngOnDestroy() {
        if (this.timer) clearInterval(this.timer);
        if (this.searchTimer) clearTimeout(this.searchTimer);
    }

    updateHeure() {
        this.heureActuelle = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    onSearch() {
        if (this.searchQuery.length < 2) { this.resultats = { dossiers: [], clients: [], actes: [] }; return; }
        clearTimeout(this.searchTimer);
        this.loading = true;
        this.showResults = true;
        this.searchTimer = setTimeout(() => this.doSearch(), 400);
    }

    doSearch() {
        const token = localStorage.getItem('token');
        const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
        const q = encodeURIComponent(this.searchQuery);

        const apiUrl = environment.apiUrl;
        let done = 0;
        const res: any = { dossiers: [], clients: [], actes: [] };

        this.http.get<any[]>(`${apiUrl}/dossiers?search=${q}`, { headers }).subscribe({
            next: (d) => { res.dossiers = (d || []).slice(0, 4); },
            error: () => {},
            complete: () => { done++; if (done === 3) { this.resultats = res; this.loading = false; } }
        });

        this.http.get<any[]>(`${apiUrl}/clients?search=${q}`, { headers }).subscribe({
            next: (d) => { res.clients = (d || []).slice(0, 4); },
            error: () => {},
            complete: () => { done++; if (done === 3) { this.resultats = res; this.loading = false; } }
        });

        this.http.get<any[]>(`${apiUrl}/actes?search=${q}`, { headers }).subscribe({
            next: (d) => { res.actes = (d || []).slice(0, 4); },
            error: () => {},
            complete: () => { done++; if (done === 3) { this.resultats = res; this.loading = false; } }
        });
    }

    naviguer(route: string) {
        this.clearSearch();
        this.router.navigate([route]);
    }

    clearSearch() {
        this.searchQuery = '';
        this.showResults = false;
        this.resultats = { dossiers: [], clients: [], actes: [] };
    }

    toggleDarkMode() {
        this.layoutService.layoutConfig.update(c => ({ ...c, darkTheme: !c.darkTheme }));
    }

    voirProfil() { this.router.navigate(['/pages/profil']); }
    voirUtilisateurs() { this.router.navigate(['/pages/roles']); }
    logout() { localStorage.clear(); this.router.navigate(['/auth/login']); }
}
