"""paiements_fix_columns

Revision ID: a1b2c3d4e5f6
Revises: de83bf854034
Create Date: 2026-06-01 00:00:00.000000

Aligne la table paiements avec le modèle :
- convertit type_paiement/mode_paiement (ENUM PostgreSQL) en VARCHAR
- normalise les valeurs en minuscules
- ajoute les colonnes optionnelles manquantes (note_caisse, etc.)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'de83bf854034'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(conn, table: str, column: str) -> bool:
    insp = sa.inspect(conn)
    return column in {c['name'] for c in insp.get_columns(table)}


def upgrade() -> None:
    conn = op.get_bind()

    op.execute(
        "ALTER TABLE paiements "
        "ALTER COLUMN type_paiement TYPE VARCHAR USING type_paiement::text"
    )
    op.execute(
        "ALTER TABLE paiements "
        "ALTER COLUMN mode_paiement TYPE VARCHAR USING mode_paiement::text"
    )

    op.execute("UPDATE paiements SET type_paiement = LOWER(type_paiement) WHERE type_paiement IS NOT NULL")
    op.execute("UPDATE paiements SET mode_paiement = LOWER(mode_paiement) WHERE mode_paiement IS NOT NULL")

    op.execute("DROP TYPE IF EXISTS typepaiement")
    op.execute("DROP TYPE IF EXISTS modepaiement")

    optional_columns = [
        ('mot_de_passe', sa.String()),
        ('numero_cheque', sa.String()),
        ('reference_virement', sa.String()),
        ('reseau_mobile', sa.String()),
        ('numero_mobile', sa.String()),
        ('autre_mode', sa.String()),
        ('note_caisse', sa.Text()),
    ]
    for name, col_type in optional_columns:
        if not _column_exists(conn, 'paiements', name):
            op.add_column('paiements', sa.Column(name, col_type, nullable=True))


def downgrade() -> None:
    conn = op.get_bind()
    if _column_exists(conn, 'paiements', 'note_caisse'):
        op.drop_column('paiements', 'note_caisse')
