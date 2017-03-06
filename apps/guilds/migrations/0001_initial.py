# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 20:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('creationdata', models.DateTimeField(default=django.utils.timezone.now)),
                ('motd', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'guilds',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuildInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'guild_invites',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuildMembership',
            fields=[
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='players.Player')),
                ('nick', models.CharField(default='', max_length=15)),
            ],
            options={
                'db_table': 'guild_membership',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuildRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('level', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'guild_ranks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuildWar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guild1', models.IntegerField(default=0)),
                ('guild2', models.IntegerField(default=0)),
                ('name1', models.CharField(max_length=255)),
                ('name2', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0)),
                ('started', models.BigIntegerField(default=0)),
                ('ended', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'guild_wars',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuildwarKill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('killer', models.CharField(max_length=50)),
                ('target', models.CharField(max_length=50)),
                ('killerguild', models.IntegerField()),
                ('targetguild', models.IntegerField()),
                ('time', models.BigIntegerField()),
            ],
            options={
                'db_table': 'guildwar_kills',
                'managed': False,
            },
        ),
    ]
