# Generated by Django 2.1.5 on 2019-04-05 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoo', '0012_remove_bids_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='bids',
            name='fileupload',
            field=models.FileField(default=False, upload_to='uploads/%Y/%m/%d/%H/%S'),
        ),
    ]