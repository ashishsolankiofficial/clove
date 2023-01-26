# Generated by Django 4.1.4 on 2023-01-25 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
        ('payable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unsettledbet',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_bets', to='team.team'),
        ),
    ]