# Generated by Django 4.2.5 on 2024-01-23 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseprovider', '0037_mentorsupportsession_passcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='mentorSupportSession',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courseprovider.mentorsupportsession'),
        ),
    ]
