# Generated by Django 5.1.2 on 2025-01-01 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category_App', '0001_initial'),
        ('JobPost_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpost',
            name='category',
            field=models.ManyToManyField(to='Category_App.category'),
        ),
    ]
