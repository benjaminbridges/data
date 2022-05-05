import django_filters
from django_filters import *
from django.forms import CheckboxSelectMultiple
from data.functions import permissionentitycheck, permissionprofilecheck
from data.models import AnswerInteger, Entity, Survey, SurveyBreakdown
from django.urls import resolve




def ents(request):
    if request is None:
        return Entity.objects.none()
    entities = permissionentitycheck(request)
    profilelist = permissionprofilecheck(request)
    current_url = resolve(request.path_info).url_name

    if current_url == 'report':
        extractlist = ['Sunday Service Attendance', 'Small Group Attendance', 'Volunteer Numbers', 'Alpha Attendance',
                       'Rising Generation Attendance', 'Social Transformation Participation']
    elif current_url == 'givingreport':
        extractlist = ['Giving and Income']
    else:
        extractlist = [""]

    if request.GET.getlist('survey', '') == "":
        x = Survey.objects.all()
    else:
        x = request.GET.getlist('survey', '')
    if request.GET.getlist('breakdown', '') == "":
        y = SurveyBreakdown.objects.all()
    else:
        y = request.GET.getlist('breakdown', '')
    return Entity.objects.filter(id__in=entities,
                                 surveyentity__surveybreakdown__surveyinstance__profile__in=profilelist).filter(
        surveyentity__survey__in=x, surveyentity__surveybreakdown__in=y, surveyentity__survey__survey_name__in=extractlist).distinct()


def suvs(request):
    if request is None:
        return Survey.objects.none()
    entities = permissionentitycheck(request)
    profilelist = permissionprofilecheck(request)
    current_url = resolve(request.path_info).url_name

    if current_url == 'report':
        extractlist = ['Sunday Service Attendance', 'Small Group Attendance', 'Volunteer Numbers', 'Alpha Attendance',
                       'Rising Generation Attendance', 'Social Transformation Participation']
    elif current_url == 'givingreport':
        extractlist = ['Giving and Income']
    else:
        extractlist = ""

    if request.GET.getlist('entity', '') == "":
        x = Entity.objects.all()
    else:
        x = request.GET.getlist('entity', '')
    if request.GET.getlist('breakdown', '') == "":
        y = SurveyBreakdown.objects.all()
    else:
        y = request.GET.getlist('breakdown', '')
    return Survey.objects.filter(surveyentity__entity__in=entities,
                                 surveyentity__surveybreakdown__surveyinstance__profile__in=profilelist).filter(
        surveyentity__entity__in=x, surveyentity__surveybreakdown__in=y, survey_name__in=extractlist).distinct()


def breaks(request):
    if request is None:
        return SurveyBreakdown.objects.none()
    entities = permissionentitycheck(request)
    profilelist = permissionprofilecheck(request)
    current_url = resolve(request.path_info).url_name

    if current_url == 'report':
        extractlist = ['Sunday Service Attendance', 'Small Group Attendance', 'Volunteer Numbers', 'Alpha Attendance',
                  'Rising Generation Attendance', 'Social Transformation Participation']
    elif current_url == 'givingreport':
        extractlist = ['Giving and Income']
    else:
        extractlist = ""

    if request.GET.getlist('entity', '') == "":
        x = Entity.objects.all()
    else:
        x = request.GET.getlist('entity', '')
    if request.GET.getlist('survey', '') == "":
        y = Survey.objects.all()
    else:
        y = request.GET.getlist('survey', '')
    return SurveyBreakdown.objects.filter(surveyentity__entity__in=entities,
                                          surveyinstance__profile__in=profilelist).filter(
        surveyentity__entity__in=x, surveyentity__survey__in=y, surveyentity__survey__survey_name__in=extractlist).values_list('surveybreakdown_category', flat=True).distinct()


class AnswerFilter(django_filters.FilterSet):
    entity = filters.ModelMultipleChoiceFilter('surveyinstance__surveybreakdown__surveyentity__entity', queryset=ents,
                                               label="Church", widget=CheckboxSelectMultiple)
    survey = filters.ModelMultipleChoiceFilter('surveyinstance__surveybreakdown__surveyentity__survey', queryset=suvs,
                                               label="Survey", widget=CheckboxSelectMultiple)
    breakdown = filters.ModelMultipleChoiceFilter('surveyinstance__surveybreakdown', queryset=breaks, label="Reminder category",
                                                  widget=CheckboxSelectMultiple)

    class Meta:
        model = AnswerInteger
        fields = '__all__'
        exclude = ['answer_integer', 'answer_status', 'surveyinstance']







def ents2(request):
    if request is None:
        return Entity.objects.none()
    entities = permissionentitycheck(request)
    profilelist = permissionprofilecheck(request)

    if request.GET.getlist('survey', '') == "":
        x = Survey.objects.all()
    else:
        x = request.GET.getlist('survey', '')
    if request.GET.getlist('breakdown', '') == "":
        y = SurveyBreakdown.objects.all()
    else:
        y = request.GET.getlist('breakdown', '')
    return Entity.objects.filter(id__in=entities,
                                 surveyentity__surveybreakdown__surveyinstance__profile__in=profilelist).filter(
        surveyentity__survey__in=x, surveyentity__surveybreakdown__in=y).distinct()


def suvs2(request):
    if request is None:
        return Survey.objects.none()
    entities = permissionentitycheck(request)
    profilelist = permissionprofilecheck(request)

    if request.GET.getlist('entity', '') == "":
        x = Entity.objects.all()
    else:
        x = request.GET.getlist('entity', '')
    if request.GET.getlist('breakdown', '') == "":
        y = SurveyBreakdown.objects.all()
    else:
        y = request.GET.getlist('breakdown', '')
    return Survey.objects.filter(surveyentity__entity__in=entities,
                                 surveyentity__surveybreakdown__surveyinstance__profile__in=profilelist).filter(
        surveyentity__entity__in=x, surveyentity__surveybreakdown__in=y).distinct()


def breaks2(request):
    if request is None:
        return SurveyBreakdown.objects.none()
    entities = permissionentitycheck(request)
    profilelist = permissionprofilecheck(request)

    if request.GET.getlist('entity', '') == "":
        x = Entity.objects.all()
    else:
        x = request.GET.getlist('entity', '')
    if request.GET.getlist('survey', '') == "":
        y = Survey.objects.all()
    else:
        y = request.GET.getlist('survey', '')
    return SurveyBreakdown.objects.filter(surveyentity__entity__in=entities,
                                          surveyinstance__profile__in=profilelist).filter(
        surveyentity__entity__in=x, surveyentity__survey__in=y).values_list('surveybreakdown_category', flat=True).distinct()


class AnswerFilter2(django_filters.FilterSet):
    entity = filters.ModelMultipleChoiceFilter('surveyinstance__surveybreakdown__surveyentity__entity', queryset=ents2,
                                               label="Church", widget=CheckboxSelectMultiple)
    survey = filters.ModelMultipleChoiceFilter('surveyinstance__surveybreakdown__surveyentity__survey', queryset=suvs2,
                                               label="Survey", widget=CheckboxSelectMultiple)
    breakdown = filters.ModelMultipleChoiceFilter('surveyinstance__surveybreakdown', queryset=breaks2, label="Reminder category",
                                                  widget=CheckboxSelectMultiple)

    class Meta:
        model = AnswerInteger
        fields = '__all__'
        exclude = ['answer_integer', 'answer_status', 'surveyinstance']
