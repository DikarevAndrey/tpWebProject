# Generated by Django 2.0.3 on 2018-03-30 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qSite', '0008_auto_20180330_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='value',
            field=models.IntegerField(choices=[(-1, 'DISLIKE'), (1, 'LIKE')], verbose_name='Like or dislike'),
        ),
    ]
