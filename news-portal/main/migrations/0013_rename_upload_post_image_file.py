# Generated by Django 4.0.2 on 2022-06-07 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_post_upload'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='upload',
            new_name='image_file',
        ),
    ]