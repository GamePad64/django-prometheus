from django.db import connections
from django.db.migrations.executor import MigrationExecutor
from prometheus_client import Gauge

unapplied_migrations = Gauge(
    'django_migrations_unapplied_total',
    'Count of unapplied migrations by database connection',
    ['connection'])

applied_migrations = Gauge(
    'django_migrations_applied_total',
    'Count of applied migrations by database connection',
    ['connection'])


def ExportMigrationsForDatabase(alias, executor):
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    unapplied_migrations.labels(alias).set(len(plan))
    applied_migrations.labels(alias).set(len(
        executor.loader.applied_migrations))


def ExportMigrations():
    """Exports counts of unapplied migrations.

    This is meant to be called during app startup, ideally by
    django_prometheus.apps.AppConfig.
    """
    for alias in connections.databases:
        executor = MigrationExecutor(connections[alias])
        ExportMigrationsForDatabase(alias, executor)
