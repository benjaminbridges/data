# Generated by Django 4.0 on 2022-04-08 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_alter_breakdowncategory_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveybreakdown',
            name='surveybreakdown_category',
            field=models.CharField(default=0, max_length=25),
            preserve_default=False,
        ),
    ]
