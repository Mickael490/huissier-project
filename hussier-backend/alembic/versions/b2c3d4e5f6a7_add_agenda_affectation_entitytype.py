"""add AGENDA and AFFECTATION to entitytype enum

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-06-01

"""
from typing import Union
from alembic import op


revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # PostgreSQL : ajout de valeurs à un type ENUM existant.
    # IF NOT EXISTS rend la migration ré-exécutable sans erreur.
    op.execute("ALTER TYPE entitytype ADD VALUE IF NOT EXISTS 'AGENDA'")
    op.execute("ALTER TYPE entitytype ADD VALUE IF NOT EXISTS 'AFFECTATION'")


def downgrade() -> None:
    # PostgreSQL ne permet pas de retirer une valeur d'un ENUM simplement.
    # Pas de downgrade : opération non réversible sans recréer le type.
    pass
