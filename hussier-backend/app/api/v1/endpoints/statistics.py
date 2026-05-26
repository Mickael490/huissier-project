from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(deps.get_db)):
    from app.models.dossier import Dossier, StatutDossier
    from app.models.client import Client
    from app.models.utilisateur import Utilisateur
    from app.models.document import Document
    from app.models.paiement import Paiement
    from app.models.agenda import Agenda

    maintenant = datetime.now()
    debut_mois = maintenant.replace(day=1, hour=0, minute=0, second=0)
    fin_semaine = maintenant + timedelta(days=7)

    total_dossiers = db.query(func.count(Dossier.id)).scalar() or 0
    dossiers_actifs = db.query(func.count(Dossier.id)).filter(Dossier.statut == StatutDossier.EN_COURS).scalar() or 0
    dossiers_nouveaux = db.query(func.count(Dossier.id)).filter(Dossier.statut == StatutDossier.NOUVEAU).scalar() or 0
    total_clients = db.query(func.count(Client.id)).scalar() or 0
    total_utilisateurs = db.query(func.count(Utilisateur.id)).scalar() or 0
    total_documents = db.query(func.count(Document.id)).scalar() or 0
    total_paiements = db.query(func.count(Paiement.id)).scalar() or 0
    paiements_mois = db.query(func.sum(Paiement.montant)).filter(Paiement.date_paiement >= debut_mois).scalar() or 0
    rdv_semaine = db.query(func.count(Agenda.id)).filter(Agenda.date_debut >= maintenant, Agenda.date_debut <= fin_semaine).scalar() or 0

    dossiers_par_type = db.query(Dossier.type_dossier, func.count(Dossier.id)).group_by(Dossier.type_dossier).all()
    dossiers_par_statut = db.query(Dossier.statut, func.count(Dossier.id)).group_by(Dossier.statut).all()

    derniers_dossiers = db.query(Dossier).order_by(Dossier.date_creation.desc()).limit(5).all()
    prochains_rdv = db.query(Agenda).filter(Agenda.date_debut >= maintenant).order_by(Agenda.date_debut).limit(5).all()
    derniers_paiements = db.query(Paiement).order_by(Paiement.date_paiement.desc()).limit(5).all()

    return {
        "kpis": {
            "total_dossiers": total_dossiers,
            "dossiers_actifs": dossiers_actifs,
            "dossiers_nouveaux": dossiers_nouveaux,
            "total_clients": total_clients,
            "total_utilisateurs": total_utilisateurs,
            "total_documents": total_documents,
            "total_paiements": total_paiements,
            "paiements_mois": float(paiements_mois),
            "rdv_semaine": rdv_semaine
        },
        "graphiques": {
            "dossiers_par_type": [{"type": str(t), "count": c} for t, c in dossiers_par_type],
            "dossiers_par_statut": [{"statut": str(s), "count": c} for s, c in dossiers_par_statut]
        },
        "derniers_dossiers": [
            {
                "id": d.id,
                "numero": d.numero_dossier,
                "objet": d.objet,
                "type": str(d.type_dossier),
                "statut": str(d.statut),
                "date": str(d.date_creation)
            } for d in derniers_dossiers
        ],
        "prochains_rdv": [
            {
                "id": r.id,
                "titre": r.titre,
                "type": str(r.type_rdv),
                "date_debut": str(r.date_debut),
                "lieu": r.lieu
            } for r in prochains_rdv
        ],
        "derniers_paiements": [
            {
                "id": p.id,
                "montant": float(p.montant),
                "type": str(p.type_paiement),
                "mode": str(p.mode_paiement),
                "date": str(p.date_paiement)
            } for p in derniers_paiements
        ]
    }
