# Generated by Django 3.1.4 on 2021-01-07 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20210107_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutdate',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.workout'),
        ),
    ]
