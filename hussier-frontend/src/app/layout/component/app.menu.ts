import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MenuItem } from 'primeng/api';
import { AppMenuitem } from './app.menuitem';

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
    role: string = '';

    ngOnInit() {
        this.role = localStorage.getItem('role') || '';
        this.buildMenu();
    }

    isAdmin(): boolean {
        return this.role?.toUpperCase() === 'ADMIN';
    }

    isHuissierOrAdmin(): boolean {
        return ['ADMIN', 'HUISSIER'].includes(this.role?.toUpperCase() || '');
    }

    buildMenu() {
        const gestionItems: any[] = [
            { label: 'Dossiers', icon: 'pi pi-fw pi-folder', routerLink: ['/pages/dossier'] },
            { label: 'Clients', icon: 'pi pi-fw pi-users', routerLink: ['/pages/client'] },
            { label: 'Parties', icon: 'pi pi-fw pi-user-plus', routerLink: ['/pages/partie'] },
            { label: 'Actes', icon: 'pi pi-fw pi-file-edit', routerLink: ['/pages/acte'] },
        ];

        if (this.isHuissierOrAdmin()) {
            gestionItems.push({ label: 'Paiements', icon: 'pi pi-fw pi-dollar', routerLink: ['/pages/paiement'] });
            gestionItems.push({ label: 'Affectations', icon: 'pi pi-fw pi-sitemap', routerLink: ['/pages/affectation'] });
        }

        const documentItems: any[] = [
            { label: 'Documents', icon: 'pi pi-fw pi-file', routerLink: ['/pages/document'] },
        ];

        if (this.isHuissierOrAdmin()) {
            documentItems.push({ label: 'Archives', icon: 'pi pi-fw pi-inbox', routerLink: ['/pages/archive'] });
        }

        this.model = [
            {
                label: 'Tableau de bord',
                items: [
                    { label: 'Dashboard', icon: 'pi pi-fw pi-home', routerLink: ['/'] }
                ]
            },
            {
                label: 'Gestion',
                items: gestionItems
            },
            {
                label: 'Documents & Archives',
                items: documentItems
            },
            {
                label: 'Planning',
                items: [
                    { label: 'Agenda', icon: 'pi pi-fw pi-calendar', routerLink: ['/pages/agenda'] },
                ]
            }
        ];

        if (this.isAdmin()) {
            this.model.push({
                label: 'Paramètres',
                items: [
                    { label: 'Cabinet', icon: 'pi pi-fw pi-building', routerLink: ['/pages/cabinet'] },
                    { label: 'Utilisateurs', icon: 'pi pi-fw pi-user', routerLink: ['/pages/utilisateur'] },
                    { label: 'Audit', icon: 'pi pi-fw pi-shield', routerLink: ['/pages/audit'] },
                ]
            });
        }
    }
}