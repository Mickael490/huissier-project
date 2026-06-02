import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { AppMenuitem } from './app.menuitem';
import { hasRole, AppRole } from 'src/services/role.guard';

@Component({
    selector: 'app-menu',
    standalone: true,
    imports: [CommonModule, AppMenuitem, RouterModule],
    template: `<ul class="layout-menu">
        <ng-container *ngFor="let item of model; let i = index">
            <li app-menuitem *ngIf="!item.separator" [item]="item" [index]="i" [root]="true"></li>
            <li *ngIf="item.separator" class="menu-separator"></li>
        </ng-container>
    </ul>`
})
export class AppMenu implements OnInit {
    model: MenuItem[] = [];

    ngOnInit() {
        this.buildMenu();
    }

    private can(roles: AppRole[]): boolean {
        return hasRole(roles);
    }

    private isAdmin(): boolean {
        return this.can(['ADMIN']);
    }

    buildMenu() {
        const gestionItems: any[] = [];
        if (this.can(['ADMIN', 'HUISSIER', 'CLERC', 'ASSISTANT'])) {
            gestionItems.push({ label: 'Dossiers', icon: 'pi pi-fw pi-folder', routerLink: ['/pages/dossier'] });
        }
        if (this.can(['ADMIN', 'HUISSIER', 'CLERC', 'SECRETAIRE'])) {
            gestionItems.push({ label: 'Clients', icon: 'pi pi-fw pi-users', routerLink: ['/pages/client'] });
        }
        if (this.can(['ADMIN', 'HUISSIER', 'CLERC'])) {
            gestionItems.push({ label: 'Parties', icon: 'pi pi-fw pi-user-plus', routerLink: ['/pages/partie'] });
            gestionItems.push({ label: 'Actes', icon: 'pi pi-fw pi-file-edit', routerLink: ['/pages/acte'] });
        }
        if (this.can(['ADMIN', 'HUISSIER'])) {
            gestionItems.push({ label: 'Paiements', icon: 'pi pi-fw pi-dollar', routerLink: ['/pages/paiement'] });
            gestionItems.push({ label: 'Affectations', icon: 'pi pi-fw pi-sitemap', routerLink: ['/pages/affectation'] });
        }

        const documentItems: any[] = [];
        if (this.can(['ADMIN', 'HUISSIER', 'CLERC', 'ASSISTANT'])) {
            documentItems.push({ label: 'Documents', icon: 'pi pi-fw pi-file', routerLink: ['/pages/document'] });
        }
        if (this.can(['ADMIN', 'HUISSIER'])) {
            documentItems.push({ label: 'Archives', icon: 'pi pi-fw pi-inbox', routerLink: ['/pages/archive'] });
        }

        this.model = [
            {
                label: 'Tableau de bord',
                items: [
                    { label: 'Dashboard', icon: 'pi pi-fw pi-home', routerLink: ['/'] }
                ]
            }
        ];

        if (gestionItems.length) {
            this.model.push({ label: 'Gestion', items: gestionItems });
        }
        if (documentItems.length) {
            this.model.push({ label: 'Documents & Archives', items: documentItems });
        }

        this.model.push({
            label: 'Planning',
            items: [
                { label: 'Agenda', icon: 'pi pi-fw pi-calendar', routerLink: ['/pages/agenda'] },
            ]
        });

        if (this.isAdmin()) {
            this.model.push({
                label: 'Paramètres',
                items: [
                    { label: 'Cabinet', icon: 'pi pi-fw pi-building', routerLink: ['/pages/cabinet'] },
                    { label: 'Utilisateurs', icon: 'pi pi-fw pi-user', routerLink: ['/pages/utilisateur'] },
                    { label: 'Rôles', icon: 'pi pi-fw pi-key', routerLink: ['/pages/roles'] },
                    { label: 'Audit', icon: 'pi pi-fw pi-shield', routerLink: ['/pages/audit'] },
                ]
            });
        }
    }
}
