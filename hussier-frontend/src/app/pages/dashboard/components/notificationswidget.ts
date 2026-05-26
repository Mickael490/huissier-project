import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
    standalone: true,
    selector: 'app-notifications-widget',
    imports: [CommonModule],
    template: `
        <div class="card">
            <div class="font-semibold text-xl mb-4">Rendez-vous à venir</div>
            <ul class="list-none p-0 m-0">
                <li *ngFor="let rdv of agendas" class="flex items-center py-3 border-b border-surface">
                    <div class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center mr-4">
                        <i class="pi pi-calendar text-purple-500"></i>
                    </div>
                    <div class="flex-1">
                        <div class="font-medium">{{ rdv.titre }}</div>
                        <div class="text-sm text-muted-color">{{ rdv.type_rdv }}</div>
                    </div>
                    <div class="text-sm text-muted-color">{{ rdv.date_debut | date:'dd/MM HH:mm' }}</div>
                </li>
            </ul>
            <div *ngIf="agendas.length === 0" class="text-center text-muted-color py-4">
                Aucun rendez-vous à venir
            </div>
        </div>
    `
})
export class NotificationsWidget implements OnInit {
    agendas: any[] = [];

    constructor(private http: HttpClient) {}

    ngOnInit() {
        const token = localStorage.getItem('token');
        const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
        this.http.get<any[]>(`${environment.apiUrl}/agendas?limit=5`, { headers }).subscribe({
            next: (data) => this.agendas = data.slice(0, 5),
            error: () => {}
        });
    }
}