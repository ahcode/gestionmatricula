# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-02 18:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='profesorVerificado',
            new_name='profesorSinVerificar',
        ),
    ]
