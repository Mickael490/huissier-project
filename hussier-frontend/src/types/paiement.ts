export enum TypePaiement {
  FRAIS = 'frais',
  AVANCE = 'avance',
  RECOUVREMENT = 'recouvrement'
}

export enum ModePaiement {
  ESPECES = 'especes',
  CHEQUE = 'cheque',
  VIREMENT = 'virement'
}

export interface Paiement {
  id: number;
  id_dossier: number;
  type_paiement: TypePaiement;
  montant: number;
  date_paiement: string;
  mode_paiement: ModePaiement;
  reverse_au_client: boolean;
}

export interface PaiementCreate {
  id_dossier: number;
  type_paiement: TypePaiement;
  montant: number;
  date_paiement: string;
  mode_paiement: ModePaiement;
  reverse_au_client: boolean;
}

export interface PaiementUpdate extends Partial<PaiementCreate> {}
