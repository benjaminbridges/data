# Generated by Django 4.0 on 2022-04-12 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0012_remove_surveybreakdown_surveybreakdown_reminder_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveybreakdown',
            name='surveybreakdown_reminder_date',
            field=models.IntegerField(default=0),
        ),
    ]
