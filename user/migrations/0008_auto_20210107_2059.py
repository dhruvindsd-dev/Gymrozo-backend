# Generated by Django 3.1.4 on 2021-01-07 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0001_initial'),
        ('user', '0007_auto_20210107_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='test',
        ),
        migrations.AlterField(
            model_name='userdata',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='instructor.instructor'),
        ),
        migrations.DeleteModel(
            name='TestDb',
        ),
    ]
