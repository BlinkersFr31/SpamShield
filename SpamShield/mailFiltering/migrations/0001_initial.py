# Generated by Django 5.0 on 2023-12-27 10:51

import mailFiltering.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('allow', models.BooleanField(default=False)),
                ('block', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Serveur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=50)),
                ('password', mailFiltering.models.pwdField()),
            ],
        ),
    ]
