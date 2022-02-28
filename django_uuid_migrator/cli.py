import os
import re
from pathlib import Path

import click


def get_migration_rank(filename):
    regex = r"(\d{4})\_[a-zA-Z0-9\s_\\.\-\(\):]+(\.py)$"
    matches = list(re.finditer(regex, filename, re.MULTILINE))
    if matches:
        number = matches[0].groups()[0]
        return int(number)


def get_last_migration(filenames):
    pairs = []
    for filename in filenames:
        rank = get_migration_rank(filename)
        if not rank:
            continue
        pairs.append((rank, filename))
    return sorted(pairs)[-1][1]


def get_last_app_migration(app_path):
    path = app_path / "migrations"
    filenames = os.listdir(path)
    return get_last_migration(filenames)


def generate_uuid_migrations(app_path, model_name):
    if not os.path.exists(app_path):
        click.echo(f"Path incorrect: {str(app_path)}")
        return

    last_migration = get_last_app_migration(app_path)
    last_migration_rank = int(last_migration.split("_")[0])
    last_migration_name = last_migration.split(".py")[0]

    migration1_name = (
        f"{last_migration_rank + 1:04}_{model_name.lower()}_add_uuid_field"
    )
    migration2_name = (
        f"{last_migration_rank + 2:04}_{model_name.lower()}_populate_uuid_values"
    )
    migration3_name = (
        f"{last_migration_rank + 3:04}_{model_name.lower()}_remove_uuid_null"
    )

    migration1_path = app_path / "migrations" / f"{migration1_name}.py"
    migration2_path = app_path / "migrations" / f"{migration2_name}.py"
    migration3_path = app_path / "migrations" / f"{migration3_name}.py"

    context = dict(
        app_name=app_path.name,
        model_name=model_name,
        model_name_lower=model_name.lower(),
        last_migration_name=last_migration_name,
        last_migration_rank=last_migration_rank,
        migration1_name=migration1_name,
        migration2_name=migration2_name,
    )

    from .templates import migration1, migration2, migration3

    migration1 = migration1.format(**context)
    migration2 = migration2.format(**context)
    migration3 = migration3.format(**context)

    with open(migration1_path, "w") as f:
        f.write(migration1)
        click.echo(f"Created {migration1_path}")
    with open(migration2_path, "w") as f:
        f.write(migration2)
        click.echo(f"Created {migration1_path}")
    with open(migration3_path, "w") as f:
        f.write(migration3)
        click.echo(f"Created {migration1_path}")


@click.command()
@click.argument("app_path", required=True)
@click.argument("model_name", required=True)
def main(app_path, model_name):
    generate_uuid_migrations(app_path=Path(app_path), model_name=model_name)
