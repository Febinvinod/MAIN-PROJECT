# Generated by Django 4.2.5 on 2024-02-05 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseprovider', '0042_remove_webinar_benefits_webinar_selected_benefits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webinar',
            name='organizer_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
