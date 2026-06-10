import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, timer } from 'rxjs';
import { tap, shareReplay, switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private cache$ = new BehaviorSubject<any>(null);
  private lastFetch = 0;
  private CACHE_DURATION = 60000; // 60 secondes

  constructor(private http: HttpClient) {}

  getDashboard(): Observable<any> {
    const now = Date.now();
    
    // Si cache valide, retourne le cache
    if (this.cache$.value && (now - this.lastFetch) < this.CACHE_DURATION) {
      return new Observable(observer => {
        observer.next(this.cache$.value);
        observer.complete();
      });
    }

    // Sinon, requête API
    return this.http.get('/api/v1/statistics/dashboard').pipe(
      tap(data => {
        this.cache$.next(data);
        this.lastFetch = now;
      }),
      shareReplay(1)
    );
  }

  // Invalide le cache (quand données changent)
  invalidateCache() {
    this.lastFetch = 0;
  }
}
