import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
    standalone: true,
    selector: 'app-stats-widget',
    imports: [CommonModule],
    template: `
        <div class="col-span-12 lg:col-span-6 xl:col-span-2">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Dossiers</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ stats.total_dossiers }}</div>
                    </div>
                    <div class="flex items-center justify-center bg-blue-100 dark:bg-blue-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-folder text-blue-500 text-xl!"></i>
                    </div>
                </div>
                <span class="text-muted-color">Total des dossiers</span>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-2">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Clients</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ stats.total_clients }}</div>
                    </div>
                    <div class="flex items-center justify-center bg-orange-100 dark:bg-orange-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-users text-orange-500 text-xl!"></i>
                    </div>
                </div>
                <span class="text-muted-color">Total des clients</span>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-2">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Utilisateurs</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ stats.total_utilisateurs }}</div>
                    </div>
                    <div class="flex items-center justify-center bg-cyan-100 dark:bg-cyan-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-user text-cyan-500 text-xl!"></i>
                    </div>
                </div>
                <span class="text-muted-color">Total des utilisateurs</span>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-2">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Documents</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ stats.total_documents }}</div>
                    </div>
                    <div class="flex items-center justify-center bg-purple-100 dark:bg-purple-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-file text-purple-500 text-xl!"></i>
                    </div>
                </div>
                <span class="text-muted-color">Total des documents</span>
            </div>
        </div>
        <div class="col-span-12 lg:col-span-6 xl:col-span-2">
            <div class="card mb-0">
                <div class="flex justify-between mb-4">
                    <div>
                        <span class="block text-muted-color font-medium mb-4">Paiements</span>
                        <div class="text-surface-900 dark:text-surface-0 font-medium text-xl">{{ stats.total_paiements }}</div>
                    </div>
                    <div class="flex items-center justify-center bg-green-100 dark:bg-green-400/10 rounded-border" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-dollar text-green-500 text-xl!"></i>
                    </div>
                </div>
                <span class="text-muted-color">Total des paiements</span>
            </div>
        </div>
    `
})
export class StatsWidget implements OnInit {
    stats = {
        total_dossiers: 0,
        total_clients: 0,
        total_utilisateurs: 0,
        total_documents: 0,
        total_paiements: 0
    };

    constructor(private http: HttpClient) {}

    ngOnInit() {
        const token = localStorage.getItem('token');
        const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
        this.http.get<any>(`${environment.apiUrl}/statistics/dashboard`, { headers }).subscribe({
            next: (data) => this.stats = data,
            error: () => {}
        });
    }
}