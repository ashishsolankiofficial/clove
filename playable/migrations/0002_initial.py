# Generated by Django 4.1.4 on 2023-01-25 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tournament', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tournament',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament', to='playable.sport'),
        ),
        migrations.AddField(
            model_name='bilateralmatch',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bilateralmatches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bilateralmatch',
            name='teamA',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ateam_matches', to='team.team'),
        ),
        migrations.AddField(
            model_name='bilateralmatch',
            name='teamB',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bteam_matches', to='team.team'),
        ),
        migrations.AddField(
            model_name='bilateralmatch',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_matches', to='playable.tournament'),
        ),
        migrations.AddField(
            model_name='bilateralmatch',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_matches', to='team.team'),
        ),
    ]
