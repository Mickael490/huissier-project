import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

export const adminGuard: CanActivateFn = () => {
  const router = inject(Router);
  const role = localStorage.getItem('role');
  if (role === 'admin') return true;
  router.navigate(['/']);
  return false;
};

export const huissierGuard: CanActivateFn = () => {
  const router = inject(Router);
  const role = localStorage.getItem('role');
  if (['admin', 'huissier'].includes(role || '')) return true;
  router.navigate(['/']);
  return false;
};

export const clercGuard: CanActivateFn = () => {
  const router = inject(Router);
  const role = localStorage.getItem('role');
  if (['admin', 'huissier', 'clerc'].includes(role || '')) return true;
  router.navigate(['/']);
  return false;
};
