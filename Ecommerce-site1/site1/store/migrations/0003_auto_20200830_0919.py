# Generated by Django 3.0.7 on 2020-08-30 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_productmdl_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmdl',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
