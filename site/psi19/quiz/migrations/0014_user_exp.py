# Generated by Django 2.2.1 on 2019-06-06 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_auto_20190606_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='exp',
            field=models.IntegerField(default=0),
        ),
    ]
