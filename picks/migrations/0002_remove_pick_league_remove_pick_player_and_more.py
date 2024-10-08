# Generated by Django 5.1.1 on 2024-09-05 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pick',
            name='league',
        ),
        migrations.RemoveField(
            model_name='pick',
            name='player',
        ),
        migrations.RemoveField(
            model_name='strike',
            name='league',
        ),
        migrations.RemoveField(
            model_name='strike',
            name='player',
        ),
        migrations.AddField(
            model_name='pick',
            name='leagueplayer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='picks.leagueplayer'),
        ),
        migrations.AddField(
            model_name='strike',
            name='leagueplayer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='picks.leagueplayer'),
        ),
    ]
