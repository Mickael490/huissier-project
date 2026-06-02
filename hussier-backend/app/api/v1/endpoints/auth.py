from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.api import deps
from app.crud import crud_utilisateur
from app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.services import audit
from app.models.audit_log import ActionType, EntityType

router = APIRouter()

@router.post("/login")
def login(
    request: Request,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Connexion et récupération du token JWT"""
    utilisateur = crud_utilisateur.get_by_email(db, email=form_data.username)
    if not utilisateur or not verify_password(form_data.password, utilisateur.mot_de_passe_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not utilisateur.actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé"
        )
    access_token = create_access_token(
        data={"sub": utilisateur.email, "role": utilisateur.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    audit.record(db, utilisateur, request, action=ActionType.LOGIN,
                 entity_type=EntityType.UTILISATEUR, entity_id=utilisateur.id,
                 description=f"Connexion de {utilisateur.email}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": utilisateur.role,
        "nom": utilisateur.nom,
        "prenom": utilisateur.prenom
    }

@router.post("/logout")
def logout():
    """Déconnexion (gérée côté frontend)"""
    return {"message": "Déconnexion réussie"}
