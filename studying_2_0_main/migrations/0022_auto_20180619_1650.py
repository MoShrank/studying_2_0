# Generated by Django 2.0.6 on 2018-06-19 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studying_2_0_main', '0021_auto_20180619_1647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectelement',
            old_name='folder_element',
            new_name='folderelement',
        ),
    ]