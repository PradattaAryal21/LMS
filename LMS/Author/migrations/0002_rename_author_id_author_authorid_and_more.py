# Generated by Django 5.1.6 on 2025-02-16 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Author', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='author_id',
            new_name='AuthorID',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='bio',
            new_name='Bio',
        ),
        migrations.RenameField(
            model_name='author',
            old_name='name',
            new_name='Name',
        ),
    ]
