# Generated by Django 2.1.5 on 2019-04-04 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoo', '0009_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=25)),
                ('lastname', models.CharField(max_length=25)),
                ('org_name', models.CharField(max_length=25)),
                ('email', models.CharField(max_length=25)),
                ('fileupload', models.FileField(upload_to='')),
                ('amount', models.IntegerField()),
            ],
        ),
    ]
