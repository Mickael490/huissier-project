export interface Cabinet {
  id: number;
  nom: string;
  raison_sociale?: string;
  adresse: string;
  code_postal?: string;
  ville?: string;
  telephone?: string;
  email?: string;
  site_web?: string;
  logo_url?: string;
  numero_agrement?: string;
  juridiction_rattachement?: string;
  chambre_departementale?: string;
  actif: boolean;
  date_creation: string;
  date_modification?: string;
}

export interface CabinetCreate {
  nom: string;
  raison_sociale?: string;
  adresse: string;
  code_postal?: string;
  ville?: string;
  telephone?: string;
  email?: string;
  site_web?: string;
  logo_url?: string;
  numero_agrement?: string;
  juridiction_rattachement?: string;
  chambre_departementale?: string;
  actif?: boolean;
}

export interface CabinetUpdate extends Partial<CabinetCreate> {}