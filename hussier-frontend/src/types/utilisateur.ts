export enum RoleEnum {
  ADMIN = 'ADMIN',
  HUISSIER = 'HUISSIER',
  CLERC = 'CLERC',
  ASSISTANT = 'ASSISTANT',
  SECRETAIRE = 'SECRETAIRE',
}

export interface Utilisateur {
  id: number;
  email: string;
  nom: string;
  prenom: string;
  telephone?: string;
  role: RoleEnum;
  actif: boolean;
  date_creation: string;
  date_modification?: string;
  derniere_connexion?: string;
}

export interface UtilisateurCreate {
  email: string;
  nom: string;
  prenom: string;
  telephone?: string;
  mot_de_passe: string;
  role?: RoleEnum;
  actif?: boolean;
  id_cabinet: number;
}

export interface UtilisateurUpdate {
  email?: string;
  nom?: string;
  prenom?: string;
  telephone?: string;
  role?: RoleEnum;
  actif?: boolean;
  mot_de_passe?: string;
}