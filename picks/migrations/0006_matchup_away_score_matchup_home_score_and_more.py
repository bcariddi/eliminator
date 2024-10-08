# Generated by Django 5.1.1 on 2024-09-05 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picks', '0005_alter_matchup_date_alter_matchup_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchup',
            name='away_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='matchup',
            name='home_score',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='matchup',
            name='home_spread',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='matchup',
            name='tie',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
