# Generated by Django 2.0.6 on 2018-06-18 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studying_2_0_main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='elements',
        ),
    ]
