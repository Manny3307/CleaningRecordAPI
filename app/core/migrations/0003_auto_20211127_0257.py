# Generated by Django 3.2.9 on 2021-11-27 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_ubercleaningrecords_uberdriver_uberdrivercar_uberdrivercontactinfo_uberdrivercpvvcertificate_uberdri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uberdriver',
            name='driver_email',
            field=models.EmailField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='ubertempcleaningrecords',
            name='driver_email',
            field=models.EmailField(max_length=200, unique=True),
        ),
    ]
