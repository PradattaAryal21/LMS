# Generated by Django 5.1.6 on 2025-02-17 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
