import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';

export type AppRole = 'ADMIN' | 'HUISSIER' | 'CLERC' | 'ASSISTANT' | 'SECRETAIRE';

const currentRole = (): string => (localStorage.getItem('role') || '').toUpperCase();

export const rolesGuard = (allowed: AppRole[]): CanActivateFn => () => {
  const router = inject(Router);
  if (allowed.includes(currentRole() as AppRole)) return true;
  router.navigate(['/pages/dashboard']);
  return false;
};

export const hasRole = (allowed: AppRole[]): boolean =>
  allowed.includes(currentRole() as AppRole);

export const adminGuard: CanActivateFn = rolesGuard(['ADMIN']);
export const huissierGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER']);
export const clercGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER', 'CLERC']);
export const assistantGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER', 'CLERC', 'ASSISTANT']);
export const secretaireGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER', 'CLERC', 'ASSISTANT', 'SECRETAIRE']);

export const dossierGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER', 'CLERC', 'ASSISTANT']);
export const clientGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER', 'CLERC', 'SECRETAIRE']);
export const partieGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER', 'CLERC']);
export const acteGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER', 'CLERC']);
export const paiementGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER']);
export const affectationGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER']);
export const documentGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER', 'CLERC', 'ASSISTANT']);
export const archiveGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER']);
export const agendaGuard: CanActivateFn = rolesGuard(['ADMIN', 'HUISSIER', 'CLERC', 'ASSISTANT', 'SECRETAIRE']);
