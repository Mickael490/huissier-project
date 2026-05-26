export enum StatutDossier {
  NOUVEAU = 'nouveau',
  EN_COURS = 'en_cours',
  EN_ATTENTE = 'en_attente',
  TERMINE = 'termine',
  ARCHIVE = 'archive',
  ANNULE = 'annule'
}

export enum TypeDossier {
  CONTENTIEUX = 'contentieux',
  RECOUVREMENT = 'recouvrement',
  CONSTAT = 'constat',
  SIGNIFICATION = 'signification',
  SAISIE = 'saisie',
  EXPULSION = 'expulsion',
  AUTRE = 'autre'
}

export interface Dossier {
  mot_de_passe?: string;
  id?: number;
  numero_dossier?: string;
  objet: string;
  description?: string;
  type_dossier: TypeDossier;
  statut?: StatutDossier;
  montant_principal?: number;
  montant_frais?: number;
  montant_total?: number;
  client_id: number;
  cabinet_id: number;
  utilisateur_responsable_id?: number;
  date_ouverture?: string;
  date_cloture?: string;
  created_at?: string;
  updated_at?: string;
}

export interface DossierCreate {
  objet: string;
  description?: string;
  type_dossier: TypeDossier;
  cabinet_id: number;
  client_id?: number;
  utilisateur_responsable_id?: number;
  montant_principal?: number;
  montant_frais?: number;
  montant_total?: number;
  date_ouverture?: string;
  date_cloture?: string;
}

export interface DossierUpdate {
  objet?: string;
  description?: string;
  type_dossier?: TypeDossier;
  statut?: StatutDossier;
  montant_principal?: number;
  montant_frais?: number;
  montant_total?: number;
  date_ouverture?: string;
  date_cloture?: string;
  mot_de_passe?: string;
  client_id?: number;
  utilisateur_responsable_id?: number;
}