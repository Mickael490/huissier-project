export enum TypeClient {
  PARTICULIER = 'particulier',
  AVOCAT = 'avocat',
  ENTREPRISE = 'entreprise',
  JURIDICTION = 'juridiction',
}

export interface Client {
  mot_de_passe?: string;
  observations?: string;
  id: number;
  cabinet_id: number;
  type_client: TypeClient;
  nom: string;
  prenom?: string;
  adresse?: string;
  telephone?: string;
  email?: string;
  siret?: string;
  representant_legal?: string;
  date_creation: string;
  date_modification?: string;
}

export interface ClientCreate {
  mot_de_passe?: string;
  cabinet_id: number;
  type_client: TypeClient;
  nom: string;
  prenom?: string;
  adresse?: string;
  telephone?: string;
  email?: string;
  siret?: string;
  representant_legal?: string;
}


export interface ClientUpdate extends Partial<ClientCreate> {}
