# Generated by Django 4.1.13 on 2024-04-19 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_additem_hsn_code_alter_additem_cost_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='additem',
            old_name='preffered_vendor',
            new_name='prefered_vendor',
        ),
    ]