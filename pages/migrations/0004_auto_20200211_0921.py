# Generated by Django 3.0.3 on 2020-02-11 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20200211_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='nationality',
            field=models.CharField(max_length=30),
        ),
    ]
