# Generated by Django 3.2.9 on 2021-12-16 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='createcleaningrecords',
            name='csv_file_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]