# Generated by Django 3.1.4 on 2021-10-25 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0011_auto_20211024_2302'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='category',
            new_name='categories',
        ),
    ]
