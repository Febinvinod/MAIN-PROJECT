# Generated by Django 4.2.5 on 2023-10-01 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseprovider', '0021_alter_internship_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='internship',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courseprovider.internship'),
        ),
    ]
