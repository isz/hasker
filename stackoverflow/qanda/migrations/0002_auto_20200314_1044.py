# Generated by Django 3.0.4 on 2020-03-14 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qanda', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='content',
            new_name='text',
        ),
    ]