# Generated by Django 3.0.6 on 2021-04-16 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vid_id', models.CharField(max_length=64, unique=True)),
                ('title', models.CharField(max_length=144)),
                ('desc', models.TextField()),
                ('published_date', models.DateTimeField()),
                ('thumbnail_url', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'Videos',
            },
        ),
    ]