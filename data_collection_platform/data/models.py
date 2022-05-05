from django.core.validators import MaxValueValidator, MinValueValidator
from djmoney.models.fields import MoneyField
from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField


site_permissions_list = [
        ('user', 'user'),
        ('centalteam', 'centalteam'),
        ('entity', 'entity'),
        ('org', 'org'),
        ('sa', 'sa')]


class Profile(models.Model):
    user = models.OneToOneField(User, null=True,  blank=True,  on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    site_permission = models.CharField(max_length=30, choices=site_permissions_list, default='user')
    entity = models.ManyToManyField('Entity', verbose_name="Church")

    class Meta:
        ordering = ['email']

    def __str__(self):
        return f"{self.user}"


class Organisation(models.Model):
    org_name = models.CharField(max_length=200, unique=True)
    org_description = models.CharField(max_length=200)
    org_color = ColorField(default='#FF0000')
    org_logo = models.ImageField()
    # org_created = models.DateField()
    # org_last_edited = models.DataField()

    def __str__(self):
        return f"ID {self.id} | {self.org_name}"


class Group(models.Model):
    group_name = models.CharField(max_length=200, unique=True)
    group_description = models.CharField(max_length=200)
    # group_created = models.DateField()
    # group_last_edited = models.DataField()

    def __str__(self):
        return f"{self.group_name}"


class Entity(models.Model):
    entity_name = models.CharField(max_length=200, unique=True)
    entity_email_primary = models.EmailField(max_length=200, null=True, blank=True,)
    entity_website = models.URLField(max_length=200, blank=True, null=True)
    entity_postcode = models.CharField(max_length=200, null=True, blank=True)
    entity_address = models.CharField(max_length=200, null=True, blank=True)
    entity_city_town = models.CharField(max_length=200, null=True, blank=True)
    entity_created = models.DateField(auto_now_add=True)
    entity_last_edited = models.DateField(auto_now=True)
    entity_status = models.BooleanField(verbose_name="Is this Church active?", default=True)
    entity_year_founded = models.IntegerField(null=True, blank=True,
                                              choices=list(zip(range(1985, 2031), range(1985, 2031))))
    org = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    group = models.ManyToManyField(Group, through='EntityGroup')

    class Meta:
        verbose_name_plural = "Entities"

    def __str__(self):
        return f"{self.entity_name}"


class EntityGroup(models.Model):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, verbose_name="Church")
    group = models.ForeignKey('Group', on_delete=models.CASCADE)


# class Category(models.Model):
#    category_name = models.CharField(max_length=200)
#    category_description = models.CharField(max_length=200)
#
#    class Meta:
#        verbose_name_plural = "Categories"
#
#    def __str__(self):
#        return f"{self.category_name}"


survey_interval_choices = [
        ('Daily', 'Daily'),
        ('Daily weekdays', 'Daily weekdays'),
        ('Weekly', 'Weekly'),
        ('Fortnightly', 'Fortnightly'),
        ('Monthly', 'Monthly'),
        ('Last day of the month', 'Last day of the month'),
        ('First working day monthly', 'First working day monthly'),
        ('Annually', 'Annually'),
        ('Previous year', 'Previous year')]


class Survey(models.Model):
    survey_name = models.CharField(verbose_name="Survey name", max_length=200)
    survey_description = models.TextField(null=True, blank=True)
#    category = models.ForeignKey('Category', on_delete=models.CASCADE,
#                                 help_text="Please select the monst relevant category")
    entity = models.ManyToManyField(Entity, verbose_name="Select churches", blank=True, through="SurveyEntity",
            help_text="You can select multiple entities by using the ctrl or shift key. To select all press ctrl & a")
    survey_entity_to_set_times = models.BooleanField(verbose_name="Allow entity to set dates, interval and occurnces",
                                                     default=False, )
    survey_interval = models.CharField(verbose_name="Interval", null=True, max_length=30,
                                       choices=survey_interval_choices, default='weekly',
                                       help_text="how regularily should this survey take place")
    survey_occurances = models.IntegerField(verbose_name="Occurances", default=1,
                                            validators=[MaxValueValidator(365), MinValueValidator(1)])
    survey_start_date = models.DateField(verbose_name="Due date", null=True)
    survey_breakdown_allowed = models.BooleanField(verbose_name="Allow church to segment this survey", default=True)
    survey_active = models.BooleanField(verbose_name="Survey active", default=True)
    survey_created_by = models.CharField(verbose_name="Created by", max_length=200)

    def __str__(self):
        return f"{self.survey_name}"


class SurveyEntity(models.Model):
    survey_interval = models.CharField(null=True, max_length=30, choices=survey_interval_choices, default='weekly',
                                       help_text="how regularily should this survey take place")
    survey_occurances = models.IntegerField(default=1, validators=[MaxValueValidator(365), MinValueValidator(1)])
    survey_start_date = models.DateField(null=True)
    survey_times_assigned = models.BooleanField(default=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Church")
    surveyentity_active = models.BooleanField(verbose_name="Survey Entity Active", default=True)

    class Meta:
        verbose_name_plural = "Survey Entities"

    def __str__(self):
        return f"{self.id} | {self.survey} | {self.entity} | {self.survey_interval} starting {self.survey_start_date}"


class SurveyBreakdown(models.Model):
    surveybreakdown_category = models.CharField(verbose_name="Category", max_length=25, null=True, blank=True)
    surveybreakdown_name = models.CharField(verbose_name="Title", max_length=200)
    surveybreakdown_time = models.TimeField(null=True, help_text="at what time should this survey take place",
                                            verbose_name="Reminder Time")
    surveybreakdown_reminder_date = models.IntegerField(default=0)
    surveyentity = models.ForeignKey(SurveyEntity, on_delete=models.CASCADE)
    profile = models.ManyToManyField('Profile', through="SurveyBreakdownProfile")
    surveybreakdown_active = models.BooleanField(verbose_name="Breakdown Active", default=True)

    def __str__(self):
        return f"{self.surveybreakdown_name}"


class SurveyBreakdownProfile(models.Model):
    surveybreakdown = models.ForeignKey(SurveyBreakdown, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    surveybreakdownprofile_active = models.BooleanField(verbose_name="Breakdown Profile Active", default=True)


class SurveyInstance(models.Model):
    survey_date = models.DateField(null=True)
    survey_start_date = models.DateField(null=True)
    survey_end_date = models.DateField(null=True)
    survey_reminder_date = models.DateField(null=True)
    survey_time = models.TimeField(null=True)
    survey_instance_complete = models.BooleanField(default=False)
    surveybreakdown = models.ForeignKey(SurveyBreakdown, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    surveyinstance_active = models.BooleanField(verbose_name="Instance Active", default=True)

    def __str__(self):
        return f"{self.id} | {self.survey_date} | {self.surveybreakdown.surveybreakdown_name} | " \
               f"{self.surveybreakdown.surveyentity.survey} | {self.surveybreakdown.surveyentity.entity} | " \
               f"{self.profile} "


question_type_choices = [
        ('Short Text', 'Short Text'),
        ('Long Text', 'Long Text'),
        ('File', 'File'),
        ('Whole Number', 'Whole Number'),
        ('Decimal Number', 'Decimal Number'),
        # ('Duration', 'Duration'),
        # ('Money', 'Money'),
        ('Date', 'Date')
        ]


class Question(models.Model):
    question_content = models.CharField(max_length=200, verbose_name="Question")
    question_type = models.CharField(max_length=20, choices=question_type_choices, default='text',
                                     verbose_name="Type")
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"ID {self.id} | Question: {self.question_content} | Type: {self.question_type}"


class BreakdownCategory(models.Model):
    category = models.CharField(max_length=25)
    category_description = models.CharField(max_length=200)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"ID {self.id} | Category: {self.category} | Survey: {self.survey}"

# Answers
# Text
# Answer short text - Character Field


class AnswerShortText(models.Model):
    answer_short_text = models.CharField(max_length=140)
    answer_status = models.BooleanField(null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    surveyinstance = models.ForeignKey('SurveyInstance', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ID {self.id} | {self.answer_short_text} "


# Answer long text - Text Field
class AnswerLongText(models.Model):
    answer_long_text = models.TextField()
    answer_status = models.BooleanField(null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    surveyinstance = models.ForeignKey('SurveyInstance', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ID {self.id} | {self.answer_long_text} "


# Files
# Answer File - File, filename, filepath, caption description
class AnswerFile(models.Model):
    answer_file = models.FileField()
    answer_file_name = models.CharField(max_length=30)
    answer_caption = models.CharField(max_length=140)
    answer_description = models.TextField(null=True)
    answer_status = models.BooleanField(null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    surveyinstance = models.ForeignKey('SurveyInstance', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ID {self.id} | {self.answer_file_name} "


# Numbers
# Answer Integer - Wholenumber
class AnswerInteger(models.Model):
    answer_integer = models.IntegerField()
    answer_status = models.BooleanField(null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    surveyinstance = models.ForeignKey('SurveyInstance', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ID {self.id} | {self.answer_integer} "


# Answer Currency - Decomal Field
class AnswerCurrency(models.Model):
    answer_currency = MoneyField(max_digits=14, decimal_places=2, default_currency='GBP')
    answer_status = models.BooleanField(null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    surveyinstance = models.ForeignKey('SurveyInstance', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ID {self.id} | {self.answer_currency} "


# Answer Decimal - Float Field
class AnswerFloat(models.Model):
    answer_float = models.FloatField()
    answer_status = models.BooleanField(null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    surveyinstance = models.ForeignKey('SurveyInstance', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ID {self.id} | {self.answer_float} "


# Time
# Answer Date
class AnswerDate(models.Model):
    answer_date = models.DateField()
    answer_status = models.BooleanField(null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    surveyinstance = models.ForeignKey('SurveyInstance', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ID {self.id} | {self.answer_date} "


# Answer Duration
class AnswerDuration(models.Model):
    answer_duration = models.DurationField()
    answer_status = models.BooleanField(null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    surveyinstance = models.ForeignKey('SurveyInstance', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ID {self.id} | {self.answer_duration} "


# if adding a new answer type then the functions in functions.py will need updateing
