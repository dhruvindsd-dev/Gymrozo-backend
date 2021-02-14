# Generated by Django 3.1.4 on 2021-01-07 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0001_initial'),
        ('user', '0006_auto_20210107_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='instructor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ma_instructor', to='instructor.instructor'),
        ),
    ]
