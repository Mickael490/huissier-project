from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.api import deps
from app.core.config import settings
from app.models.agenda import Agenda, StatutRendezVous
from app.services.email import envoyer_email, template_rappel_echeance

router = APIRouter()


@router.post("/rappels-echeances")
def envoyer_rappels_echeances(
    secret: str = Query(..., description="Cle secrete cron"),
    heures_avant: int = Query(24, ge=1, le=168),
    db: Session = Depends(deps.get_db),
):
    """
    Envoie un email de rappel pour chaque rendez-vous planifie dans les
    prochaines `heures_avant` heures, non encore notifie et non annule.
    Destine a etre appele par un service cron externe (ex: cron-job.org),
    protege par une cle secrete plutot que par une authentification JWT.
    """
    if secret != settings.CRON_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Cle secrete invalide")

    maintenant = datetime.utcnow()
    limite = maintenant + timedelta(hours=heures_avant)

    rendez_vous = (
        db.query(Agenda)
        .filter(
            Agenda.date_debut >= maintenant,
            Agenda.date_debut <= limite,
            Agenda.statut == StatutRendezVous.PLANIFIE,
            Agenda.annule == False,
            Agenda.notification_envoyee == False,
        )
        .all()
    )

    envoyes = 0
    erreurs = 0

    for rdv in rendez_vous:
        destinataires = []
        if rdv.client and rdv.client.email:
            destinataires.append(rdv.client.email)
        if rdv.utilisateur and rdv.utilisateur.email:
            destinataires.append(rdv.utilisateur.email)

        if not destinataires:
            continue

        corps = template_rappel_echeance(
            titre=rdv.titre,
            date_debut=rdv.date_debut.strftime("%d/%m/%Y a %H:%M"),
            lieu=rdv.lieu or "",
        )

        succes = True
        for destinataire in destinataires:
            ok = envoyer_email(destinataire, f"Rappel - {rdv.titre}", corps)
            succes = succes and ok

        if succes:
            rdv.notification_envoyee = True
            envoyes += 1
        else:
            erreurs += 1

    db.commit()

    return {
        "rendez_vous_trouves": len(rendez_vous),
        "rappels_envoyes": envoyes,
        "erreurs": erreurs,
    }
