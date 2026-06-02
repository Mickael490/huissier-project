// src/environments/environment.prod.ts
// AVANT DE BUILDER POUR LA PROD : remplacer apiUrl par l'URL reelle du backend.
// Cette URL doit AUSSI figurer dans BACKEND_CORS_ORIGINS cote backend (.env).
export const environment = {
  production: true,
  apiUrl: 'https://api.mondomaine.com/api/v1'
};
