# Generated by Django 2.0.3 on 2018-05-09 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qSite', '0019_auto_20180509_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='questions', to='qSite.Tag', verbose_name='Tags of the question'),
        ),
    ]