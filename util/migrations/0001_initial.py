# Generated by Django 4.1.4 on 2023-01-10 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ext_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]