from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import de la configuration Alembic
config = context.config

# Configuration du logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import de Base et des modèles
from app.db.session import Base

# ✅ Importer TES 12 modèles
from app.models.cabinet import Cabinet
from app.models.utilisateur import Utilisateur
from app.models.client import Client
from app.models.dossier import Dossier
from app.models.affectation_dossier import AffectationDossier
from app.models.partie import Partie
from app.models.agenda import Agenda
from app.models.acte import Acte
from app.models.paiement import Paiement
from app.models.archive import Archive
from app.models.audit_log import AuditLog
from app.models.statistic import Statistic

# Métadonnées pour l'autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
