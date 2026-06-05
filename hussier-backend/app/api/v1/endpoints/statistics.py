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
    from app.models.agenda import Agenda, StatutRendezVous
    from app.models.acte import Acte
    from app.models.partie import Partie
    from app.models.archive import Archive
    from app.models.audit_log import AuditLog

    # Dates de reference (naive local, comme la DB)
    maintenant = datetime.now()
    debut_jour = maintenant.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_jour = debut_jour + timedelta(days=1)
    debut_mois = maintenant.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    fin_semaine = maintenant + timedelta(days=7)
    # Bornes du mois precedent / suivant (pour le comparatif)
    debut_mois_prec = (debut_mois - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    debut_mois_suiv = (debut_mois + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # --- KPIs principaux ---
    total_dossiers = db.query(func.count(Dossier.id)).scalar() or 0
    dossiers_actifs = db.query(func.count(Dossier.id)).filter(Dossier.statut == StatutDossier.EN_COURS).scalar() or 0
    dossiers_nouveaux = db.query(func.count(Dossier.id)).filter(Dossier.statut == StatutDossier.NOUVEAU).scalar() or 0
    dossiers_termines = db.query(func.count(Dossier.id)).filter(Dossier.statut == StatutDossier.TERMINE).scalar() or 0
    total_clients = db.query(func.count(Client.id)).scalar() or 0
    total_utilisateurs = db.query(func.count(Utilisateur.id)).scalar() or 0
    total_documents = db.query(func.count(Document.id)).scalar() or 0
    total_actes = db.query(func.count(Acte.id)).scalar() or 0
    total_parties = db.query(func.count(Partie.id)).scalar() or 0
    total_archives = db.query(func.count(Archive.id)).scalar() or 0
    total_paiements = db.query(func.count(Paiement.id)).scalar() or 0
    paiements_mois = db.query(func.sum(Paiement.montant)).filter(Paiement.date_paiement >= debut_mois.date()).scalar() or 0

    # RDV : aujourd'hui = jour calendaire complet ; semaine = 7 prochains jours
    rdv_aujourd_hui = db.query(func.count(Agenda.id)).filter(
        Agenda.date_debut >= debut_jour,
        Agenda.date_debut < fin_jour,
        Agenda.annule == False
    ).scalar() or 0
    rdv_semaine = db.query(func.count(Agenda.id)).filter(
        Agenda.date_debut >= debut_jour,
        Agenda.date_debut <= fin_semaine,
        Agenda.annule == False
    ).scalar() or 0

    # --- Comparatif mois en cours vs mois precedent ---
    dossiers_mois = db.query(func.count(Dossier.id)).filter(Dossier.date_creation >= debut_mois).scalar() or 0
    dossiers_mois_prec = db.query(func.count(Dossier.id)).filter(Dossier.date_creation >= debut_mois_prec, Dossier.date_creation < debut_mois).scalar() or 0
    clients_mois = db.query(func.count(Client.id)).filter(Client.date_creation >= debut_mois).scalar() or 0
    clients_mois_prec = db.query(func.count(Client.id)).filter(Client.date_creation >= debut_mois_prec, Client.date_creation < debut_mois).scalar() or 0
    paiements_mois_prec = db.query(func.sum(Paiement.montant)).filter(Paiement.date_paiement >= debut_mois_prec.date(), Paiement.date_paiement < debut_mois.date()).scalar() or 0
    rdv_mois = db.query(func.count(Agenda.id)).filter(Agenda.date_debut >= debut_mois, Agenda.date_debut < debut_mois_suiv).scalar() or 0
    rdv_mois_prec = db.query(func.count(Agenda.id)).filter(Agenda.date_debut >= debut_mois_prec, Agenda.date_debut < debut_mois).scalar() or 0

    # --- Graphiques ---
    dossiers_par_type = db.query(Dossier.type_dossier, func.count(Dossier.id)).group_by(Dossier.type_dossier).all()
    dossiers_par_statut = db.query(Dossier.statut, func.count(Dossier.id)).group_by(Dossier.statut).all()

    # --- Heatmap d'activite : 4 semaines x 7 jours (Lun..Dim) a partir des logs ---
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
        semaine = 3 - (jours_ecoules // 7)
        jour = date_action.weekday()
        heatmap_activite[semaine][jour] += 1

    # --- Dernieres actions (feed) ---
    dernieres_actions = db.query(AuditLog).order_by(AuditLog.date_action.desc()).limit(8).all()

    # --- Dossiers avec delai critique : RDV a venir dans moins de 7 jours ---
    # On s'appuie sur l'agenda (echeances reelles) en excluant les RDV annules
    # et les dossiers deja termines/archives/annules.
    rdv_urgents = db.query(Agenda, Dossier).join(Dossier, Agenda.id_dossier == Dossier.id).filter(
        Agenda.date_debut >= maintenant,
        Agenda.date_debut <= fin_semaine,
        Agenda.annule == False,
        Dossier.statut.notin_([StatutDossier.TERMINE, StatutDossier.ARCHIVE, StatutDossier.ANNULE])
    ).order_by(Agenda.date_debut).all()

    dossiers_urgents = []
    deja_vus = set()
    for rdv, dossier in rdv_urgents:
        if dossier.id in deja_vus:
            continue
        deja_vus.add(dossier.id)
        jours_restants = max(0, (rdv.date_debut.date() - maintenant.date()).days)
        dossiers_urgents.append({
            "id": dossier.id,
            "numero": dossier.numero_dossier,
            "objet": dossier.objet,
            "jours_restants": jours_restants,
            "echeance": rdv.date_debut.isoformat() if rdv.date_debut else None
        })

    # --- Listes ---
    derniers_dossiers = db.query(Dossier).order_by(Dossier.date_creation.desc()).limit(5).all()
    prochains_rdv = db.query(Agenda).filter(
        Agenda.date_debut >= debut_jour,
        Agenda.annule == False
    ).order_by(Agenda.date_debut).limit(5).all()
    derniers_paiements = db.query(Paiement).order_by(Paiement.date_paiement.desc()).limit(5).all()

    return {
        "kpis": {
            "total_dossiers": total_dossiers,
            "dossiers_actifs": dossiers_actifs,
            "dossiers_nouveaux": dossiers_nouveaux,
            "dossiers_termines": dossiers_termines,
            "total_clients": total_clients,
            "total_utilisateurs": total_utilisateurs,
            "total_documents": total_documents,
            "total_actes": total_actes,
            "total_parties": total_parties,
            "total_archives": total_archives,
            "total_paiements": total_paiements,
            "paiements_mois": float(paiements_mois),
            "rdv_semaine": rdv_semaine,
            "rdv_aujourd_hui": rdv_aujourd_hui
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
        "dossiers_urgents": dossiers_urgents,
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
                "lieu": r.lieu if hasattr(r, 'lieu') else "N/A"
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

@router.get("/notifications")
def get_notifications(db: Session = Depends(deps.get_db)):
    from app.models.agenda import Agenda
    from app.models.dossier import Dossier, StatutDossier

    maintenant = datetime.now()
    dans_2_jours = maintenant + timedelta(days=2)

    rdv_proches = db.query(Agenda).filter(
        Agenda.date_debut >= maintenant,
        Agenda.date_debut <= dans_2_jours
    ).count()

    dossiers_urgents = db.query(Dossier).filter(
        Dossier.statut == StatutDossier.EN_COURS
    ).count()

    notifications = []

    if rdv_proches > 0:
        notifications.append({
            "type": "info",
            "title": f"{rdv_proches} RDV dans 2 jours",
            "message": "À confirmer ou reporter",
            "count": rdv_proches
        })

    if dossiers_urgents > 0:
        notifications.append({
            "type": "warning",
            "title": f"{dossiers_urgents} dossier(s) en cours",
            "message": "À suivre",
            "count": dossiers_urgents
        })

    return {"notifications": notifications, "total": len(notifications)}
