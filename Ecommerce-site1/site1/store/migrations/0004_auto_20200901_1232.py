# Generated by Django 3.0.7 on 2020-09-01 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200830_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmdl',
            name='price',
            field=models.FloatField(),
        ),
    ]