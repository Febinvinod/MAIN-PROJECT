# Generated by Django 4.2.5 on 2023-10-04 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courseprovider', '0031_uservideo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uservideoprogress',
            name='user',
        ),
        migrations.RemoveField(
            model_name='uservideoprogress',
            name='video',
        ),
        migrations.DeleteModel(
            name='CompletionCertificate',
        ),
        migrations.DeleteModel(
            name='UserVideoProgress',
        ),
    ]
