# Generated by Django 2.0.6 on 2018-06-18 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studying_2_0_main', '0010_auto_20180618_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectelement',
            name='elements',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studying_2_0_main.ProjectElement'),
        ),
    ]
