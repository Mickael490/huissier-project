# hussier-backend/seed_demo_data.py
#
# Nettoie les donnees metier (dossiers, clients, parties, actes, paiements,
# agenda, affectations, documents, archives) et les remplace par un jeu de
# donnees realiste et coherent pour la demonstration de soutenance.
#
# NE TOUCHE JAMAIS : cabinets, utilisateurs (comptes de connexion preserves).
#
# Usage :
#   cd hussier-backend
#   source .venv/bin/activate
#   python seed_demo_data.py

import sys
from datetime import date, datetime, timedelta

from sqlalchemy import text

from app.db.session import SessionLocal
from app.models.cabinet import Cabinet
from app.models.utilisateur import Utilisateur
from app.models.client import Client, TypeClient
from app.models.dossier import Dossier, TypeDossier, StatutDossier
from app.models.partie import Partie, RolePartie
from app.models.acte import Acte, TypeActe
from app.models.paiement import Paiement
from app.models.agenda import Agenda, TypeRendezVous, StatutRendezVous, PrioriteRendezVous

TABLES_A_VIDER = [
    "documents",
    "affectations_dossier",
    "archives",
    "paiements",
    "parties",
    "actes",
    "agenda",
    "dossiers",
    "clients",
]


def confirmer(db):
    url = str(db.get_bind().url)
    host = url.split("@")[-1] if "@" in url else url
    print(f"\nBase ciblee : {host}")
    print("Tables qui seront videes :", ", ".join(TABLES_A_VIDER))
    print("Tables PRESERVEES (non touchees) : cabinets, utilisateurs\n")
    reponse = input("Tapez CONFIRMER en majuscules pour continuer : ")
    if reponse.strip() != "CONFIRMER":
        print("Annule. Aucune modification effectuee.")
        sys.exit(0)


def vider_tables(db):
    for table in TABLES_A_VIDER:
        db.execute(text(f"DELETE FROM {table}"))
    db.commit()
    print("Tables videes.")


def main():
    db = SessionLocal()
    confirmer(db)
    vider_tables(db)

    cabinet = db.query(Cabinet).first()
    if not cabinet:
        print("ERREUR : aucun cabinet trouve en base. Impossible de continuer.")
        sys.exit(1)

    utilisateurs = db.query(Utilisateur).filter(Utilisateur.actif == True).all()
    if not utilisateurs:
        print("ERREUR : aucun utilisateur actif trouve en base.")
        sys.exit(1)
    responsable_principal = utilisateurs[0]

    def prochain_user(i):
        return utilisateurs[i % len(utilisateurs)]

    # ---------- CLIENTS ----------
    clients_data = [
        dict(type_client=TypeClient.PARTICULIER, nom="TRAORE", prenom="Amidou",
             adresse="Secteur 15, Ouagadougou", telephone="+226 70 12 34 56",
             email="amidou.traore@gmail.com"),
        dict(type_client=TypeClient.PARTICULIER, nom="KABORE", prenom="Aminata",
             adresse="Secteur 7, Ouagadougou", telephone="+226 76 45 12 33",
             email="aminata.kabore@yahoo.fr"),
        dict(type_client=TypeClient.ENTREPRISE, nom="Etablissements SANOU et Fils",
             adresse="Zone industrielle, Bobo-Dioulasso", telephone="+226 20 98 11 45",
             email="contact@sanoufils.bf", siret="BF2019B01042"),
        dict(type_client=TypeClient.PARTICULIER, nom="SAWADOGO", prenom="Rasmane",
             adresse="Secteur 30, Ouagadougou", telephone="+226 78 22 41 09",
             email="r.sawadogo@outlook.com"),
        dict(type_client=TypeClient.AVOCAT, nom="OUEDRAOGO", prenom="Justine",
             adresse="Avenue Kwame Nkrumah, Ouagadougou", telephone="+226 25 30 44 12",
             email="cabinet.ouedraogo.avocat@gmail.com", representant_legal="Me Justine OUEDRAOGO"),
        dict(type_client=TypeClient.ENTREPRISE, nom="Banque Atlantique Burkina Faso",
             adresse="Avenue de la Nation, Ouagadougou", telephone="+226 25 33 88 00",
             email="recouvrement@atlanticbank.bf", siret="BF2005B00087"),
    ]
    clients = []
    for data in clients_data:
        c = Client(id_cabinet=cabinet.id, **data)
        db.add(c)
        clients.append(c)
    db.flush()
    print(f"{len(clients)} clients crees.")

    # ---------- DOSSIERS + PARTIES + ACTES + PAIEMENTS ----------
    aujourdhui = date.today()

    dossiers_data = [
        dict(numero="DOS-2026-0001", objet="Recouvrement de creance commerciale",
             type_dossier=TypeDossier.RECOUVREMENT, statut=StatutDossier.EN_COURS,
             client=clients[2], montant=1850000,
             partie=("SOCIETE DIALLO TRANSPORT", RolePartie.DEBITEUR, "Zone industrielle, Ouagadougou"),
             acte=(TypeActe.COMMANDEMENT, "Commandement de payer delivre", "Siege social du debiteur"),
             paiement=("provision", 250000, "virement")),
        dict(numero="DOS-2026-0002", objet="Signification de jugement civil",
             type_dossier=TypeDossier.SIGNIFICATION, statut=StatutDossier.TERMINE,
             client=clients[0], montant=420000,
             partie=("COMPAORE Issouf", RolePartie.DESTINATAIRE, "Secteur 22, Ouagadougou"),
             acte=(TypeActe.SIGNIFICATION, "Jugement signifie a personne", "Domicile du destinataire"),
             paiement=("emolument", 45000, "especes")),
        dict(numero="DOS-2026-0003", objet="Constat d'etat des lieux locatif",
             type_dossier=TypeDossier.CONSTAT, statut=StatutDossier.EN_COURS,
             client=clients[3], montant=180000,
             partie=("KONATE Salif", RolePartie.AUTRE, "Secteur 30, Ouagadougou"),
             acte=(TypeActe.CONSTAT, "Constat contradictoire dresse", "Appartement loue, Secteur 30"),
             paiement=("provision", 90000, "mobile_money")),
        dict(numero="DOS-2026-0004", objet="Saisie-attribution sur compte bancaire",
             type_dossier=TypeDossier.SAISIE, statut=StatutDossier.EN_ATTENTE,
             client=clients[5], montant=3200000,
             partie=("ETS NIKIEMA COMMERCE", RolePartie.DEBITEUR, "Marche central, Ouagadougou"),
             acte=(TypeActe.SAISIE, "Saisie notifiee a l'etablissement bancaire", "Agence teneur de compte"),
             paiement=("provision", 400000, "virement")),
        dict(numero="DOS-2026-0005", objet="Expulsion locative pour impayes",
             type_dossier=TypeDossier.EXPULSION, statut=StatutDossier.NOUVEAU,
             client=clients[1], montant=650000,
             partie=("ZOUNGRANA Paul", RolePartie.DEBITEUR, "Secteur 7, Ouagadougou"),
             acte=(TypeActe.COMMANDEMENT, "Commandement de quitter les lieux", "Logement loue, Secteur 7"),
             paiement=("provision", 150000, "cheque")),
        dict(numero="DOS-2026-0006", objet="Recouvrement d'honoraires impayes",
             type_dossier=TypeDossier.CONTENTIEUX, statut=StatutDossier.EN_COURS,
             client=clients[4], montant=980000,
             partie=("SANFO Boureima", RolePartie.DEBITEUR, "Secteur 12, Ouagadougou"),
             acte=(TypeActe.PROCES_VERBAL, "Proces-verbal de carence dresse", "Domicile du debiteur"),
             paiement=("emolument", 98000, "especes")),
        dict(numero="DOS-2026-0007", objet="Signification d'assignation en justice",
             type_dossier=TypeDossier.SIGNIFICATION, statut=StatutDossier.TERMINE,
             client=clients[3], montant=310000,
             partie=("Tribunal de Grande Instance de Ouagadougou", RolePartie.DESTINATAIRE,
                     "Avenue de l'Independance, Ouagadougou"),
             acte=(TypeActe.SIGNIFICATION, "Assignation signifiee dans les delais legaux", "Greffe du tribunal"),
             paiement=("emolument", 35000, "virement")),
        dict(numero="DOS-2026-0008", objet="Recouvrement de loyers impayes",
             type_dossier=TypeDossier.RECOUVREMENT, statut=StatutDossier.ARCHIVE,
             client=clients[3], montant=540000,
             partie=("OUATTARA Fatoumata", RolePartie.DEBITEUR, "Secteur 30, Ouagadougou"),
             acte=(TypeActe.RECOUVREMENT, "Recouvrement amiable abouti", "Domicile de la debitrice"),
             paiement=("remboursement", 540000, "mobile_money")),
        dict(numero="DOS-2026-0009", objet="Constat de malfacons sur chantier",
             type_dossier=TypeDossier.CONSTAT, statut=StatutDossier.EN_COURS,
             client=clients[2], montant=275000,
             partie=("ENTREPRISE BTP FASO", RolePartie.AUTRE, "Zone industrielle, Bobo-Dioulasso"),
             acte=(TypeActe.CONSTAT, "Constat photographique et descriptif dresse", "Chantier, Bobo-Dioulasso"),
             paiement=("provision", 137500, "virement")),
        dict(numero="DOS-2026-0010", objet="Saisie mobiliere conservatoire",
             type_dossier=TypeDossier.SAISIE, statut=StatutDossier.NOUVEAU,
             client=clients[0], montant=890000,
             partie=("YAMEOGO Adama", RolePartie.DEBITEUR, "Secteur 15, Ouagadougou"),
             acte=(TypeActe.SAISIE, "Inventaire des biens saisissables en cours", "Domicile du debiteur"),
             paiement=("provision", 120000, "especes")),
    ]

    for i, d in enumerate(dossiers_data):
        jours_offset = -30 + i * 5
        dossier = Dossier(
            numero_dossier=d["numero"],
            objet=d["objet"],
            type_dossier=d["type_dossier"],
            statut=d["statut"],
            montant_principal=d["montant"],
            montant_frais=round(d["montant"] * 0.08, 2),
            montant_total=round(d["montant"] * 1.08, 2),
            client_id=d["client"].id,
            cabinet_id=cabinet.id,
            utilisateur_responsable_id=prochain_user(i).id,
            date_ouverture=datetime.utcnow() + timedelta(days=jours_offset),
        )
        db.add(dossier)
        db.flush()

        nom_p, role_p, adresse_p = d["partie"]
        db.add(Partie(id_dossier=dossier.id, nom=nom_p, role=role_p,
                       adresse=adresse_p, contact="+226 7" + str(10 + i) + " 00 00 00"))

        type_acte, resultat_acte, lieu_acte = d["acte"]
        db.add(Acte(id_dossier=dossier.id, type_acte=type_acte,
                     date_acte=aujourdhui + timedelta(days=jours_offset + 3),
                     lieu=lieu_acte, resultat=resultat_acte,
                     observations="Dossier traite conformement a la procedure legale en vigueur."))

        type_paiement, montant_paiement, mode_paiement = d["paiement"]
        db.add(Paiement(id_dossier=dossier.id, type_paiement=type_paiement,
                         montant=montant_paiement,
                         date_paiement=aujourdhui + timedelta(days=jours_offset + 1),
                         mode_paiement=mode_paiement, reverse_au_client=False))

    db.commit()
    print(f"{len(dossiers_data)} dossiers crees, avec parties, actes et paiements associes.")

    # ---------- AGENDA ----------
    rdv_data = [
        ("Audience Tribunal de Grande Instance", TypeRendezVous.AUDIENCE, 2, 9, 0, "Tribunal de Grande Instance, Ouagadougou"),
        ("Signification terrain - Secteur 12", TypeRendezVous.SIGNIFICATION, 3, 10, 30, "Secteur 12, Ouagadougou"),
        ("Rendez-vous client - suivi dossier", TypeRendezVous.CLIENT, 4, 14, 0, "Cabinet Me SAWADOGO"),
        ("Constat terrain - malfacons chantier", TypeRendezVous.CONSTAT, 5, 8, 30, "Bobo-Dioulasso"),
        ("Reunion interne - point hebdomadaire", TypeRendezVous.INTERNE, 6, 16, 0, "Cabinet Me SAWADOGO"),
    ]
    for i, (titre, type_rdv, jours, h, m, lieu) in enumerate(rdv_data):
        debut = datetime.utcnow() + timedelta(days=jours)
        debut = debut.replace(hour=h, minute=m, second=0, microsecond=0)
        db.add(Agenda(
            reference=f"RDV-2026-{i+1:03d}",
            id_dossier=None,
            id_utilisateur=prochain_user(i).id,
            titre=titre,
            type_rdv=type_rdv,
            statut=StatutRendezVous.PLANIFIE,
            priorite=PrioriteRendezVous.NORMALE,
            date_debut=debut,
            date_fin=debut + timedelta(hours=1),
            duree_minutes=60,
            lieu=lieu,
        ))
    db.commit()
    print(f"{len(rdv_data)} rendez-vous crees dans l'agenda.")

    print("\nTermine. Base de donnees prete pour la demonstration.")
    db.close()


if __name__ == "__main__":
    main()
