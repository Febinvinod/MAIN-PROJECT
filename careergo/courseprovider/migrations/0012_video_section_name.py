# Generated by Django 4.2.4 on 2023-09-22 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseprovider', '0011_remove_oncourse_video_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='section_name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
