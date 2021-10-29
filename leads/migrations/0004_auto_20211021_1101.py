# Generated by Django 3.1.4 on 2021-10-21 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_auto_20211016_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organisor',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='organisation',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
        ),
    ]