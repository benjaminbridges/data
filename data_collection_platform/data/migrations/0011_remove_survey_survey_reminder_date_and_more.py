# Generated by Django 4.0 on 2022-04-12 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_rename_survey_reminder_date_surveybreakdown_surveybreakdown_reminder_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='survey_reminder_date',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='survey_time',
        ),
        migrations.AlterField(
            model_name='surveybreakdown',
            name='surveybreakdown_category',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='surveybreakdown',
            name='surveybreakdown_name',
            field=models.CharField(max_length=200, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='surveybreakdown',
            name='surveybreakdown_reminder_date',
            field=models.DateField(help_text='On which day of the week does this activity take place?', null=True, verbose_name='Reminder Date'),
        ),
        migrations.AlterField(
            model_name='surveybreakdown',
            name='surveybreakdown_time',
            field=models.TimeField(help_text='at what time should this survey take place', null=True, verbose_name='Reminder Time'),
        ),
    ]
