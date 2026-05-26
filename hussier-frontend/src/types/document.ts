export enum TypeDocument {
  ACTE = 'acte',
  JUGEMENT = 'jugement',
  CONTRAT = 'contrat',
  COURRIER = 'courrier',
  RAPPORT = 'rapport',
  AUTRE = 'autre'
}

export interface Document {
  id: number;
  titre: string;
  type_document: TypeDocument;
  description?: string;
  fichier_url?: string;
  dossier_id?: number;
  date_creation: string;
  date_modification?: string;
}

export interface DocumentCreate {
  titre: string;
  type_document: TypeDocument;
  description?: string;
  fichier_url?: string;
  dossier_id?: number;
}

export interface DocumentUpdate extends Partial<DocumentCreate> {}
