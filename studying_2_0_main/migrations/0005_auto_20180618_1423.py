# Generated by Django 2.0.6 on 2018-06-18 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studying_2_0_main', '0004_project_elements'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='elements',
        ),
        migrations.AddField(
            model_name='projectelement',
            name='elements',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='studying_2_0_main.ProjectElement'),
        ),
        migrations.AddField(
            model_name='projectelement',
            name='project',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='studying_2_0_main.Project'),
        ),
    ]