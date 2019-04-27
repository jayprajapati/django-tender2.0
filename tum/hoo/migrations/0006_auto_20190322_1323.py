# Generated by Django 2.1.5 on 2019-03-22 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoo', '0005_auto_20190322_1303'),
    ]

    operations = [
        migrations.CreateModel(
            name='document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('document_description', models.TextField()),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
            ],
        ),
        migrations.RemoveField(
            model_name='tender',
            name='document_description',
        ),
        migrations.RemoveField(
            model_name='tender',
            name='document_name',
        ),
        migrations.AddField(
            model_name='tender',
            name='documents',
            field=models.ManyToManyField(to='hoo.document'),
        ),
    ]