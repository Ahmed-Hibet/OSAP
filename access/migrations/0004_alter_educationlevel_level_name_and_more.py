# Generated by Django 4.0.1 on 2022-05-04 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0003_alter_educationlevel_level_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationlevel',
            name='level_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='work_type',
            field=models.CharField(max_length=100),
        ),
    ]
