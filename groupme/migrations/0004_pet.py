# Generated by Django 2.2.16 on 2020-12-27 02:56

from django.db import migrations, models
import groupme.models


class Migration(migrations.Migration):

    dependencies = [
        ('groupme', '0003_auto_20201220_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('birthdate', models.DateField(db_index=True)),
                ('type', models.CharField(choices=[('dog', 'Dog'), ('cat', 'Cat')], max_length=64)),
            ],
            bases=(models.Model, groupme.models.BirthdayMixin),
        ),
    ]
