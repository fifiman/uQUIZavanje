# Generated by Django 2.2.1 on 2019-05-25 10:14

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('level', models.IntegerField(default=0)),
                ('picture', models.TextField(blank=True, default=' ', max_length=50, null=True)),
                ('banned', models.TextField(blank=True, default='', max_length=50, null=True)),
                ('ranking', models.IntegerField(default=-1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(max_length=100)),
                ('is_valid', models.BooleanField(default=False)),
                ('answer_one', models.TextField(max_length=20)),
                ('answer_two', models.TextField(max_length=20)),
                ('answer_three', models.TextField(max_length=20)),
                ('answer_four', models.TextField(max_length=20)),
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
                ('second_friend_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='friendship_f2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
