# Generated by Django 4.0.1 on 2022-04-03 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_alter_user_roll'),
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyrequirement',
            name='education_levels',
            field=models.ManyToManyField(to='access.EducationLevel'),
        ),
        migrations.AlterField(
            model_name='surveyrequirement',
            name='occupations',
            field=models.ManyToManyField(to='access.Occupation'),
        ),
    ]
