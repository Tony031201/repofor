# Generated by Django 5.0.4 on 2024-05-08 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='code_1',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='code_1_used',
            field=models.BooleanField(default=False),
        ),
    ]
