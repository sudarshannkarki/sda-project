# Generated by Django 3.0.7 on 2020-08-21 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmdl',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
