import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
    standalone: true,
    selector: 'app-best-selling-widget',
    imports: [CommonModule],
    template: `
        <div class="card mb-8!">
            <div class="font-semibold text-xl mb-4">Clients récents</div>
            <ul class="list-none p-0 m-0">
                <li *ngFor="let client of clients" class="flex items-center py-3 border-b border-surface">
                    <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center mr-4">
                        <i class="pi pi-user text-blue-500"></i>
                    </div>
                    <div class="flex-1">
                        <div class="font-medium">{{ client.nom }} {{ client.prenom }}</div>
                        <div class="text-sm text-muted-color">{{ client.type_client }}</div>
                    </div>
                    <div class="text-sm text-muted-color">{{ client.telephone }}</div>
                </li>
            </ul>
            <div *ngIf="clients.length === 0" class="text-center text-muted-color py-4">
                Aucun client enregistré
            </div>
        </div>
    `
})
export class BestSellingWidget implements OnInit {
    clients: any[] = [];

    constructor(private http: HttpClient) {}

    ngOnInit() {
        const token = localStorage.getItem('token');
        const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
        this.http.get<any[]>(`${environment.apiUrl}/clients?limit=5`, { headers }).subscribe({
            next: (data) => this.clients = data.slice(0, 5),
            error: () => {}
        });
    }
}