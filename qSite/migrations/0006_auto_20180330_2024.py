# Generated by Django 2.0.3 on 2018-03-30 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qSite', '0005_auto_20180330_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='value',
            field=models.IntegerField(choices=[(-1, 'DISLIKE'), (1, 'LIKE'), (2, 'LLike')], verbose_name='Like or dislike'),
        ),
    ]
