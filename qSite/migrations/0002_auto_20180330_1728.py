# Generated by Django 2.0.3 on 2018-03-30 17:28

from django.db import migrations
import qSite.managers


class Migration(migrations.Migration):

    dependencies = [
        ('qSite', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='profile',
            managers=[
                ('objects', qSite.managers.UserManager()),
            ],
        ),
    ]