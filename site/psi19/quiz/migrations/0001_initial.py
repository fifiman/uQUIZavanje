# Generated by Django 2.2.1 on 2019-05-23 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('level', models.IntegerField()),
                ('picture', models.TextField(max_length=50)),
                ('banned', models.TextField(max_length=50)),
                ('is_moderator', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('ranking', models.IntegerField(default=-1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=100)),
                ('is_valid', models.BooleanField(default=False)),
                ('answer_one', models.TextField(max_length=100)),
                ('answer_two', models.TextField(max_length=100)),
                ('answer_three', models.TextField(max_length=100)),
                ('answer_four', models.TextField(max_length=100)),
                ('correct', models.IntegerField()),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_one_pts', models.IntegerField()),
                ('player_two_pts', models.IntegerField()),
                ('player_three_pts', models.IntegerField()),
                ('player_four_pts', models.IntegerField()),
                ('winner', models.IntegerField()),
                ('player_four', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='game_p4', to=settings.AUTH_USER_MODEL)),
                ('player_one', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='game_p1', to=settings.AUTH_USER_MODEL)),
                ('player_three', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='game_p3', to=settings.AUTH_USER_MODEL)),
                ('player_two', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='game_p2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_friend_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='friendship_f1', to=settings.AUTH_USER_MODEL)),
                ('second_friend_id', models.ForeignKey(default=-1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='friendship_f2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
