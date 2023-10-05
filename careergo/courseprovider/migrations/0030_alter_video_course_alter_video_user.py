# Generated by Django 4.2.5 on 2023-10-04 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courseprovider', '0029_alter_video_course_alter_video_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_course', to='courseprovider.oncourse'),
        ),
        migrations.AlterField(
            model_name='video',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
