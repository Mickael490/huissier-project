import { Component, OnInit } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { LayoutService } from '../service/layout.service';

@Component({
    selector: 'app-topbar',
    standalone: true,
    imports: [RouterModule, CommonModule],
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

        <div class="layout-topbar-actions" style="display:flex; align-items:center; gap:8px;">

            <!-- Heure -->
            <div style="background:rgba(255,255,255,0.08); border-radius:8px; padding:6px 12px; display:flex; align-items:center; gap:6px;">
                <i class="pi pi-clock" style="color:#64a0c8; font-size:13px;"></i>
                <span style="color:#e2e8f0; font-size:13px; font-weight:600; font-family:monospace;">{{ heureActuelle }}</span>
            </div>

            <!-- Utilisateur -->
            <div style="background:rgba(255,255,255,0.08); border-radius:8px; padding:6px 12px; display:flex; align-items:center; gap:8px;">
                <div style="width:28px; height:28px; border-radius:50%; background:linear-gradient(135deg, #2d6a9f, #4f46e5); display:flex; align-items:center; justify-content:center; color:white; font-size:11px; font-weight:700;">
                    {{ initiales }}
                </div>
                <div>
                    <div style="font-size:13px; font-weight:600; color:white; line-height:1.2;">{{ nomUtilisateur }}</div>
                    <div style="font-size:10px; color:#64a0c8; text-transform:uppercase; letter-spacing:1px;">{{ roleUtilisateur }}</div>
                </div>
            </div>

            <!-- Profil -->
            <button type="button" (click)="voirProfil()" pTooltip="Mon profil"
                style="width:36px; height:36px; border-radius:8px; background:rgba(255,255,255,0.08); border:none; color:#e2e8f0; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                <i class="pi pi-user" style="font-size:15px;"></i>
            </button>

            <!-- Roles -->
            <button type="button" (click)="voirUtilisateurs()" pTooltip="Gestion roles"
                style="width:36px; height:36px; border-radius:8px; background:rgba(255,255,255,0.08); border:none; color:#e2e8f0; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                <i class="pi pi-shield" style="font-size:15px;"></i>
            </button>

            <!-- Theme -->
            <button type="button" (click)="toggleDarkMode()" pTooltip="Changer theme"
                style="width:36px; height:36px; border-radius:8px; background:rgba(255,255,255,0.08); border:none; color:#e2e8f0; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                <i [class]="layoutService.isDarkTheme() ? 'pi pi-sun' : 'pi pi-moon'" style="font-size:15px;"></i>
            </button>

            <!-- Deconnexion -->
            <button type="button" (click)="logout()" pTooltip="Se deconnecter"
                style="width:36px; height:36px; border-radius:8px; background:rgba(239,68,68,0.2); border:1px solid rgba(239,68,68,0.3); color:#fca5a5; cursor:pointer; display:flex; align-items:center; justify-content:center;">
                <i class="pi pi-sign-out" style="font-size:15px;"></i>
            </button>

        </div>
    </div>
    `
})
export class AppTopbar implements OnInit {
    nomUtilisateur = '';
    roleUtilisateur = '';
    initiales = '';
    heureActuelle = '';
    private timer: any;

    constructor(public layoutService: LayoutService, private router: Router) {}

    ngOnInit() {
        const nom = localStorage.getItem('nom') || '';
        const prenom = localStorage.getItem('prenom') || '';
        this.nomUtilisateur = (prenom + ' ' + nom).trim() || 'Utilisateur';
        this.roleUtilisateur = localStorage.getItem('role') || '';
        this.initiales = ((prenom.charAt(0)) + (nom.charAt(0))).toUpperCase() || 'U';
        this.updateHeure();
        this.timer = setInterval(() => this.updateHeure(), 1000);
    }

    ngOnDestroy() {
        if (this.timer) clearInterval(this.timer);
    }

    updateHeure() {
        this.heureActuelle = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    toggleDarkMode() {
        this.layoutService.layoutConfig.update(c => ({ ...c, darkTheme: !c.darkTheme }));
    }

    voirProfil() {
        this.router.navigate(['/pages/profil']);
    }

    voirUtilisateurs() {
        this.router.navigate(['/pages/roles']);
    }

    logout() {
        localStorage.clear();
        this.router.navigate(['/auth/login']);
    }
}
