# Generated by Django 4.2.5 on 2023-09-23 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': [('set_published_status', 'Can set the status of the post to either publish or not')]},
        ),
        migrations.AddField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]
