import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Client, ClientCreate, ClientUpdate } from 'src/types/client';

@Injectable({
  providedIn: 'root',
})
export class ClientService {
  private apiUrl = `${environment.apiUrl}/clients`;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  getClients(): Observable<Client[]> {
    return this.http.get<Client[]>(this.apiUrl, { headers: this.getHeaders() });
  }

  getClient(id: number): Observable<Client> {
    return this.http.get<Client>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }

  createClient(client: ClientCreate): Observable<Client> {
    return this.http.post<Client>(this.apiUrl, client, { headers: this.getHeaders() });
  }

  updateClient(id: number, client: ClientUpdate): Observable<Client> {
    return this.http.put<Client>(`${this.apiUrl}/${id}`, client, { headers: this.getHeaders() });
  }

  deleteClient(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }
}
