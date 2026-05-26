import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Document, DocumentCreate, DocumentUpdate } from 'src/types/document';

@Injectable({
  providedIn: 'root',
})
export class DocumentService {
  private apiUrl = `${environment.apiUrl}/documents`;

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  getDocuments(): Observable<Document[]> {
    return this.http.get<Document[]>(this.apiUrl, { headers: this.getHeaders() });
  }

  getDocument(id: number): Observable<Document> {
    return this.http.get<Document>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }

  createDocument(document: DocumentCreate): Observable<Document> {
    return this.http.post<Document>(this.apiUrl, document, { headers: this.getHeaders() });
  }

  updateDocument(id: number, document: DocumentUpdate): Observable<Document> {
    return this.http.put<Document>(`${this.apiUrl}/${id}`, document, { headers: this.getHeaders() });
  }

  deleteDocument(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`, { headers: this.getHeaders() });
  }
}
