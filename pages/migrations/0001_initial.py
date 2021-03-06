# Generated by Django 3.0 on 2020-02-10 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('max_student', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.School')),
            ],
        ),
    ]
