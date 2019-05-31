# Generated by Django 2.2.1 on 2019-05-31 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20190529_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_text', models.TextField(max_length=200)),
                ('reported', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='report_f2', to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='report_f1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
