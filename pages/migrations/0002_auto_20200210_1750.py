# Generated by Django 3.0 on 2020-02-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.CharField(editable=False, max_length=20, primary_key=True, serialize=False),
        ),
    ]
