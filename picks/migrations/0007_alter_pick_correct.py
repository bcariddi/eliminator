# Generated by Django 5.1.1 on 2024-09-05 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picks', '0006_matchup_away_score_matchup_home_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pick',
            name='correct',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
