# Generated by Django 5.0.4 on 2024-05-05 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_remove_post_userprofile_post_lovepoint'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='lovepoint',
            new_name='love_point',
        ),
    ]