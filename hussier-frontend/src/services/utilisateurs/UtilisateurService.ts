import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Utilisateur, UtilisateurCreate, UtilisateurUpdate } from 'src/types/utilisateur';

@Injectable({
  providedIn: 'root',
})
export class UtilisateurService {
  private apiUrl = `${environment.apiUrl}/utilisateurs`;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  getUtilisateurs(): Observable<Utilisateur[]> {
    return this.http.get<Utilisateur[]>(this.apiUrl, { headers: this.getHeaders() });
  }

  getUtilisateur(id: number): Observable<Utilisateur> {
    return this.http.get<Utilisateur>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }

  createUtilisateur(utilisateur: UtilisateurCreate): Observable<Utilisateur> {
    return this.http.post<Utilisateur>(this.apiUrl, utilisateur, { headers: this.getHeaders() });
  }

  updateUtilisateur(id: number, utilisateur: UtilisateurUpdate): Observable<Utilisateur> {
    return this.http.put<Utilisateur>(`${this.apiUrl}/${id}`, utilisateur, { headers: this.getHeaders() });
  }

  deleteUtilisateur(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }
}
