import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError, retry, timeout, TimeoutError, tap } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const token = localStorage.getItem('token');
  const authReq = token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req;

  return next(authReq).pipe(
    timeout(30000),
    retry({ count: 1, delay: 2000 }),

    catchError((error) => {
      if (error instanceof TimeoutError) {
        showToast('Serveur inaccessible. Vérifiez votre connexion internet.', 'error');
        return throwError(() => error);
      }
      const httpError = error as HttpErrorResponse;
      if (httpError.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        router.navigate(['/auth/login']);
        showToast('Session expirée. Veuillez vous reconnecter.', 'warn');
        return throwError(() => error);
      }
      if (httpError.status === 403) {
        showToast("Accès refusé. Vous n\'avez pas les droits nécessaires.", 'error');
        return throwError(() => error);
      }
      if (httpError.status === 500) {
        showToast('Erreur serveur. Veuillez réessayer plus tard.', 'error');
        return throwError(() => error);
      }
      if (httpError.status === 404) {
        showToast('Ressource introuvable.', 'warn');
        return throwError(() => error);
      }
      if (httpError.status === 0) {
        showToast('Serveur inaccessible. Vérifiez votre connexion internet.', 'error');
        return throwError(() => error);
      }
      showToast('Une erreur est survenue. Veuillez réessayer.', 'error');
      return throwError(() => error);
    })
  );
};

function showToast(message: string, severity: string) {
  const event = new CustomEvent('app-toast', {
    detail: {
      severity,
      summary: severity === 'success' ? 'Succès' : severity === 'error' ? 'Erreur' : 'Attention',
      detail: message,
      life: severity === 'success' ? 2500 : 4000
    }
  });
  window.dispatchEvent(event);
}
