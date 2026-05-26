import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DossierService {
  private apiUrl = `${environment.apiUrl}/dossiers`;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  getDossiers(skip = 0, limit = 100, cabinetId?: number, clientId?: number, statut?: string, type?: string): Observable<any> {
    let params = new HttpParams().set('skip', skip).set('limit', limit);
    if (cabinetId) params = params.set('cabinet_id', cabinetId);
    if (clientId) params = params.set('client_id', clientId);
    if (statut) params = params.set('statut', statut);
    if (type) params = params.set('type_affaire', type);
    return this.http.get<any>(this.apiUrl, { headers: this.getHeaders(), params });
  }

  getDossier(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }

  createDossier(dossier: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, dossier, { headers: this.getHeaders() });
  }

  updateDossier(id: number, dossier: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/${id}`, dossier, { headers: this.getHeaders() });
  }

  deleteDossier(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }

  getCabinets(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/cabinets`, { headers: this.getHeaders() });
  }

  getClients(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/clients`, { headers: this.getHeaders() });
  }

  getUtilisateurs(): Observable<any[]> {
    return this.http.get<any[]>(`${environment.apiUrl}/utilisateurs`, { headers: this.getHeaders() });
  }
}
