import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Paiement, PaiementCreate, PaiementUpdate } from 'src/types/paiement';

@Injectable({ providedIn: 'root' })
export class PaiementService {
  private apiUrl = `${environment.apiUrl}/paiements`;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  getPaiements(): Observable<Paiement[]> {
    return this.http.get<Paiement[]>(this.apiUrl, { headers: this.getHeaders() });
  }

  createPaiement(paiement: PaiementCreate): Observable<Paiement> {
    return this.http.post<Paiement>(this.apiUrl, paiement, { headers: this.getHeaders() });
  }

  updatePaiement(id: number, paiement: PaiementUpdate): Observable<Paiement> {
    return this.http.put<Paiement>(`${this.apiUrl}/${id}`, paiement, { headers: this.getHeaders() });
  }

  deletePaiement(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }
}