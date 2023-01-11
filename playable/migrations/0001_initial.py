# Generated by Django 4.1.4 on 2023-01-10 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament', to='playable.sport')),
            ],
        ),
    ]
