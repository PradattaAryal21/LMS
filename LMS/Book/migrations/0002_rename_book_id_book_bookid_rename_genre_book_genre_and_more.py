# Generated by Django 5.1.6 on 2025-02-17 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='book_id',
            new_name='BookId',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='genre',
            new_name='Genre',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='isbn',
            new_name='ISBN',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='quantity',
            new_name='Quantity',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='title',
            new_name='Title',
        ),
    ]
