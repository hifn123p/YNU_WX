# Generated by Django 2.0.4 on 2018-06-09 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openID', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_id', models.IntegerField(default=0)),
                ('openID', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('openID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=50)),
                ('avatarUrl', models.CharField(max_length=100)),
            ],
        ),
    ]
