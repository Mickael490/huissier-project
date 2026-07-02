from fastapi import APIRouter, Depends
from app.api import deps
from app.models.utilisateur import RoleEnum
from app.api.v1.endpoints import cabinets, clients, utilisateurs, dossiers, parties, actes, documents, archives, agendas, audit_logs, statistics, affectation_dossiers, auth, paiements, notifications

api_router = APIRouter()

# Raccourcis de rôles (alignés sur les guards du frontend : src/services/role.guard.ts)
ADMIN = RoleEnum.ADMIN
HUISSIER = RoleEnum.HUISSIER
CLERC = RoleEnum.CLERC
ASSISTANT = RoleEnum.ASSISTANT
SECRETAIRE = RoleEnum.SECRETAIRE


def roles(*allowed):
    """Dépendance d'autorisation pour un routeur entier."""
    return [Depends(deps.require_roles(*allowed))]


# Auth : public (login/logout)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Toute personne authentifiée (dashboard / statistiques)
api_router.include_router(
    statistics.router, prefix="/statistics", tags=["statistics"],
    dependencies=[Depends(deps.get_current_active_user)],
)

# Administration : ADMIN uniquement
api_router.include_router(
    cabinets.router, prefix="/cabinets", tags=["cabinets"],
    dependencies=roles(ADMIN),
)
api_router.include_router(
    utilisateurs.router, prefix="/utilisateurs", tags=["utilisateurs"],
    dependencies=roles(ADMIN),
)
api_router.include_router(
    audit_logs.router, prefix="/audit_logs", tags=["audit_logs"],
    dependencies=roles(ADMIN),
)

# Gestion métier (matrice identique au frontend)
api_router.include_router(
    clients.router, prefix="/clients", tags=["clients"],
    dependencies=roles(ADMIN, HUISSIER, CLERC, SECRETAIRE),
)
api_router.include_router(
    dossiers.router, prefix="/dossiers", tags=["dossiers"],
    dependencies=roles(ADMIN, HUISSIER, CLERC, ASSISTANT),
)
api_router.include_router(
    parties.router, prefix="/parties", tags=["parties"],
    dependencies=roles(ADMIN, HUISSIER, CLERC),
)
api_router.include_router(
    actes.router, prefix="/actes", tags=["actes"],
    dependencies=roles(ADMIN, HUISSIER, CLERC),
)
api_router.include_router(
    paiements.router, prefix="/paiements", tags=["paiements"],
    dependencies=roles(ADMIN, HUISSIER),
)
api_router.include_router(
    affectation_dossiers.router, prefix="/affectations", tags=["affectation_dossiers"],
    dependencies=roles(ADMIN, HUISSIER),
)
api_router.include_router(
    documents.router, prefix="/documents", tags=["documents"],
    dependencies=roles(ADMIN, HUISSIER, CLERC, ASSISTANT),
)
api_router.include_router(
    archives.router, prefix="/archives", tags=["archives"],
    dependencies=roles(ADMIN, HUISSIER),
)
api_router.include_router(
    agendas.router, prefix="/agendas", tags=["agendas"],
    dependencies=roles(ADMIN, HUISSIER, CLERC, ASSISTANT, SECRETAIRE),
)
# Cron externe uniquement : protege par cle secrete (voir notifications.py), pas par JWT
api_router.include_router(
    notifications.router, prefix="/notifications", tags=["notifications"],
)
