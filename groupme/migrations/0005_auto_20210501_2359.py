# Generated by Django 2.2.16 on 2021-05-02 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupme', '0004_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='weather',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='weather',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
    ]
