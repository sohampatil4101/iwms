# Generated by Django 4.1.13 on 2024-04-12 15:41

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='warehouseuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyname', models.TextField()),
                ('fullname', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
                ('phone_no', models.IntegerField()),
                ('country', models.TextField()),
                ('state', models.TextField()),
                ('terms_conditions', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('image', models.ImageField(upload_to=app.models.upload_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.warehouseuser')),
            ],
        ),
    ]