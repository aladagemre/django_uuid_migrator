migration1 = """# -*- coding: utf-8 -*-
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('{app_name}', '{last_migration_name}'),
    ]

    operations = [
        migrations.AddField(
            model_name='{model_name_lower}',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]

"""

migration2 = """# -*- coding: utf-8 -*-
from django.db import migrations
import uuid

def gen_uuid(apps, schema_editor):
    {model_name} = apps.get_model('{app_name}', '{model_name}')
    for row in {model_name}.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])

class Migration(migrations.Migration):

    dependencies = [
        ('{app_name}', '{migration1_name}'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]

"""

migration3 = """# -*- coding: utf-8 -*-
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('{app_name}', '{migration2_name}'),
    ]

    operations = [
        migrations.AlterField(
            model_name='{model_name_lower}',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]

"""
