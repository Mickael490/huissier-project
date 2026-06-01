import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

export const adminGuard: CanActivateFn = () => {
  const router = inject(Router);
  const role = (localStorage.getItem('role') || '').toUpperCase();
  if (role === 'ADMIN') return true;
  router.navigate(['/pages/dashboard']);
  return false;
};

export const huissierGuard: CanActivateFn = () => {
  const router = inject(Router);
  const role = (localStorage.getItem('role') || '').toUpperCase();
  if (['ADMIN', 'HUISSIER'].includes(role)) return true;
  router.navigate(['/pages/dashboard']);
  return false;
};

export const clercGuard: CanActivateFn = () => {
  const router = inject(Router);
  const role = (localStorage.getItem('role') || '').toUpperCase();
  if (['ADMIN', 'HUISSIER', 'CLERC'].includes(role)) return true;
  router.navigate(['/pages/dashboard']);
  return false;
};

export const secretaireGuard: CanActivateFn = () => {
  const router = inject(Router);
  const role = (localStorage.getItem('role') || '').toUpperCase();
  if (['ADMIN', 'HUISSIER', 'CLERC', 'ASSISTANT', 'SECRETAIRE'].includes(role)) return true;
  router.navigate(['/pages/dashboard']);
  return false;
};
