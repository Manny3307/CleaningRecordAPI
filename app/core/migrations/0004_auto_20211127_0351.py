# Generated by Django 3.2.9 on 2021-11-27 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20211127_0257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uberdrivercpvvcertificate',
            name='id',
        ),
        migrations.AlterField(
            model_name='uberdrivercpvvcertificate',
            name='driver_certificate_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]