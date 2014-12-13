# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Move',
            fields=[
                ('session_id', models.CharField(max_length=36)),
                ('insert_id', models.AutoField(serialize=False, primary_key=True)),
                ('player', models.CharField(max_length=1)),
                ('position', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
