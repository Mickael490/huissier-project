import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Cabinet, CabinetCreate } from 'src/types/cabinet';

@Injectable({
  providedIn: 'root'
})
export class CabinetService {
  private apiUrl = `${environment.apiUrl}/cabinets`;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  getCabinets(): Observable<Cabinet[]> {
    return this.http.get<Cabinet[]>(this.apiUrl, { headers: this.getHeaders() });
  }

  getCabinet(id: number): Observable<Cabinet> {
    return this.http.get<Cabinet>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }

  createCabinet(cabinet: CabinetCreate): Observable<Cabinet> {
    return this.http.post<Cabinet>(this.apiUrl, cabinet, { headers: this.getHeaders() });
  }

  updateCabinet(id: number, cabinet: Partial<CabinetCreate>): Observable<Cabinet> {
    return this.http.put<Cabinet>(`${this.apiUrl}/${id}`, cabinet, { headers: this.getHeaders() });
  }

  deleteCabinet(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }
}