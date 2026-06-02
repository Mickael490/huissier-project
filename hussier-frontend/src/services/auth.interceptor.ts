import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

/**
 * Ajoute automatiquement le token JWT (Authorization: Bearer ...) à chaque
 * requête HTTP, et redirige vers la page de connexion si le backend répond
 * 401 (token absent / expiré / invalide).
 *
 * Indispensable depuis que le backend impose l'authentification sur tous
 * les endpoints (voir hussier-backend/app/api/v1/api.py).
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const token = localStorage.getItem('token');

  const authReq = token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req;

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        router.navigate(['/auth/login']);
      }
      return throwError(() => error);
    })
  );
};
