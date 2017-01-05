# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-31 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matriculaasignatura',
            old_name='nota',
            new_name='nota1',
        ),
        migrations.AddField(
            model_name='matriculaasignatura',
            name='matriculaHonor1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matriculaasignatura',
            name='matriculaHonor2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matriculaasignatura',
            name='noPresentado1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matriculaasignatura',
            name='noPresentado2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='matriculaasignatura',
            name='nota2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='curso',
            name='year',
            field=models.IntegerField(choices=[(2011, '2011/2012'), (2012, '2012/2013'), (2013, '2013/2014'), (2014, '2014/2015'), (2015, '2015/2016'), (2016, '2016/2017'), (2017, '2017/2018'), (2018, '2018/2019'), (2019, '2019/2020'), (2020, '2020/2021')], unique=True),
        ),
    ]
