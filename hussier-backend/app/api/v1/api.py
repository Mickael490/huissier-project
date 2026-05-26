from fastapi import APIRouter
from app.api.v1.endpoints import cabinets, clients, utilisateurs, dossiers, parties, actes, documents, archives, agendas, audit_logs, statistics, affectation_dossiers, auth, paiements

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(cabinets.router, prefix="/cabinets", tags=["cabinets"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(utilisateurs.router, prefix="/utilisateurs", tags=["utilisateurs"])
api_router.include_router(dossiers.router, prefix="/dossiers", tags=["dossiers"])
api_router.include_router(parties.router, prefix="/parties", tags=["parties"])
api_router.include_router(actes.router, prefix="/actes", tags=["actes"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(archives.router, prefix="/archives", tags=["archives"])
api_router.include_router(agendas.router, prefix="/agendas", tags=["agendas"])
api_router.include_router(audit_logs.router, prefix="/audit_logs", tags=["audit_logs"])
api_router.include_router(affectation_dossiers.router, prefix="/affectations", tags=["affectation_dossiers"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
api_router.include_router(paiements.router, prefix="/paiements", tags=["paiements"])
