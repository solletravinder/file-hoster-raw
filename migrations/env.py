from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import os

# This is the Alembic Config object, which provides access to values within the .ini file
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Add your model's metadata here for 'autogenerate' support
from app import db, app  # Replace 'your_app' with your actual Flask app module
target_metadata = db.metadata

if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option("sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"])

# Register custom dialect for SQLiteCloud
from alembic.ddl.impl import DefaultImpl
import alembic.ddl.impl as impl

class SQLiteCloudImpl(DefaultImpl):
    __dialect__ = 'sqlitecloud'

impl._impls['sqlitecloud'] = SQLiteCloudImpl

def run_migrations_offline():
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

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()