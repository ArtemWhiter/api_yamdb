# Generated by Django 2.2.16 on 2022-04-14 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Category',
        ),
        migrations.RenameModel(
            old_name='Categorie',
            new_name='Review',
        ),
    ]
