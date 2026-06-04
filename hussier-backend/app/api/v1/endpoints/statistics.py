from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(deps.get_db)):
    from app.models.dossier import Dossier, StatutDossier
    from app.models.client import Client
    from app.models.utilisateur import Utilisateur
    from app.models.document import Document
    from app.models.paiement import Paiement
    from app.models.agenda import Agenda
    from app.models.audit_log import AuditLog

    maintenant = datetime.now(timezone.utc).replace(tzinfo=None)
    debut_mois = maintenant.replace(day=1, hour=0, minute=0, second=0)
    fin_semaine = maintenant + timedelta(days=7)
    demain = maintenant + timedelta(days=1)
    # Bornes du mois precedent et du mois suivant (pour le comparatif).
    debut_mois_prec = (debut_mois - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    debut_mois_suiv = (debut_mois + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    total_dossiers = db.query(func.count(Dossier.id)).scalar() or 0
    dossiers_actifs = db.query(func.count(Dossier.id)).filter(Dossier.statut == StatutDossier.EN_COURS).scalar() or 0
    dossiers_nouveaux = db.query(func.count(Dossier.id)).filter(Dossier.statut == StatutDossier.NOUVEAU).scalar() or 0
    total_clients = db.query(func.count(Client.id)).scalar() or 0
    total_utilisateurs = db.query(func.count(Utilisateur.id)).scalar() or 0
    total_documents = db.query(func.count(Document.id)).scalar() or 0
    total_paiements = db.query(func.count(Paiement.id)).scalar() or 0
    paiements_mois = db.query(func.sum(Paiement.montant)).filter(Paiement.date_paiement >= debut_mois).scalar() or 0
    rdv_semaine = db.query(func.count(Agenda.id)).filter(Agenda.date_debut >= maintenant, Agenda.date_debut <= fin_semaine).scalar() or 0
    rdv_aujourd_hui = db.query(func.count(Agenda.id)).filter(Agenda.date_debut >= maintenant, Agenda.date_debut < demain).scalar() or 0
    dossiers_termines = db.query(func.count(Dossier.id)).filter(Dossier.statut == StatutDossier.TERMINE).scalar() or 0

    # --- Comparatif mois en cours vs mois precedent (donnees reelles) ---
    dossiers_mois = db.query(func.count(Dossier.id)).filter(Dossier.date_creation >= debut_mois).scalar() or 0
    dossiers_mois_prec = db.query(func.count(Dossier.id)).filter(Dossier.date_creation >= debut_mois_prec, Dossier.date_creation < debut_mois).scalar() or 0
    clients_mois = db.query(func.count(Client.id)).filter(Client.date_creation >= debut_mois).scalar() or 0
    clients_mois_prec = db.query(func.count(Client.id)).filter(Client.date_creation >= debut_mois_prec, Client.date_creation < debut_mois).scalar() or 0
    paiements_mois_prec = db.query(func.sum(Paiement.montant)).filter(Paiement.date_paiement >= debut_mois_prec.date(), Paiement.date_paiement < debut_mois.date()).scalar() or 0
    rdv_mois = db.query(func.count(Agenda.id)).filter(Agenda.date_debut >= debut_mois, Agenda.date_debut < debut_mois_suiv).scalar() or 0
    rdv_mois_prec = db.query(func.count(Agenda.id)).filter(Agenda.date_debut >= debut_mois_prec, Agenda.date_debut < debut_mois).scalar() or 0

    dossiers_par_type = db.query(Dossier.type_dossier, func.count(Dossier.id)).group_by(Dossier.type_dossier).all()
    dossiers_par_statut = db.query(Dossier.statut, func.count(Dossier.id)).group_by(Dossier.statut).all()

    # Heatmap d'activite : grille 4 semaines x 7 jours (Lun..Dim) construite
    # a partir des actions reelles enregistrees dans les logs d'audit.
    debut_heatmap = maintenant - timedelta(days=28)
    logs_heatmap = db.query(AuditLog.date_action).filter(AuditLog.date_action >= debut_heatmap).all()
    heatmap_activite = [[0] * 7 for _ in range(4)]
    aujourdhui = maintenant.date()
    for (date_action,) in logs_heatmap:
        if not date_action:
            continue
        jours_ecoules = (aujourdhui - date_action.date()).days
        if jours_ecoules < 0 or jours_ecoules > 27:
            continue
        semaine = 3 - (jours_ecoules // 7)  # ligne 3 = semaine en cours (en bas)
        jour = date_action.weekday()        # 0 = lundi ... 6 = dimanche
        heatmap_activite[semaine][jour] += 1

    dernieres_actions = db.query(AuditLog).order_by(AuditLog.date_action.desc()).limit(8).all()

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
            "rdv_semaine": rdv_semaine,
            "rdv_aujourd_hui": rdv_aujourd_hui,
            "dossiers_termines": dossiers_termines
        },
        "graphiques": {
            "dossiers_par_type": [{"type": str(t), "count": c} for t, c in dossiers_par_type],
            "dossiers_par_statut": [{"statut": str(s), "count": c} for s, c in dossiers_par_statut]
        },
        "comparatif": {
            "dossiers": {"actuel": dossiers_mois, "precedent": dossiers_mois_prec},
            "clients": {"actuel": clients_mois, "precedent": clients_mois_prec},
            "paiements": {"actuel": float(paiements_mois), "precedent": float(paiements_mois_prec)},
            "rdv": {"actuel": rdv_mois, "precedent": rdv_mois_prec}
        },
        "heatmap_activite": heatmap_activite,
        "dernieres_actions": [
            {
                "action": a.action.value if a.action else None,
                "entity_type": a.entity_type.value if a.entity_type else None,
                "description": a.description,
                "date": a.date_action.isoformat() if a.date_action else None
            } for a in dernieres_actions
        ],
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
                "date_debut": r.date_debut.isoformat() if r.date_debut else None,
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
