# Generated by Django 2.2.1 on 2019-06-06 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0012_merge_20190606_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamequestions',
            name='p1_pts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gamequestions',
            name='p2_pts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gamequestions',
            name='p3_pts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gamequestions',
            name='p4_pts',
            field=models.IntegerField(default=0),
        ),
    ]
