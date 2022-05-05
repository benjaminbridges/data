import django_filters
from .models import *
from data.functions import permissionentitycheck, permissionprofilecheck
from django.forms import CheckboxSelectMultiple
from django_filters import *


def ents(request):
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
    if request.GET.getlist('profile', '') == "":
        z = Profile.objects.all()
    else:
        z = request.GET.getlist('profile', '')
    return Entity.objects.filter(id__in=entities,
                                 surveyentity__surveybreakdown__surveyinstance__profile__in=profilelist).filter(
        surveyentity__survey__in=x, surveyentity__surveybreakdown__in=y,
        surveyentity__surveybreakdown__surveyinstance__profile__in=z).distinct()


def ents2(request):
    if request is None:
        return Entity.objects.none()
    entities = permissionentitycheck(request)
    if request.GET.getlist('survey', '') == "":
        x = Survey.objects.all()
    else:
        x = request.GET.getlist('survey', '')
    return Entity.objects.filter(id__in=entities).filter(surveyentity__survey__in=x).distinct()


def suvs(request):
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
    if request.GET.getlist('profile', '') == "":
        z = Profile.objects.all()
    else:
        z = request.GET.getlist('profile', '')
    return Survey.objects.filter(surveyentity__entity__in=entities,
                                 surveyentity__surveybreakdown__surveyinstance__profile__in=profilelist).filter(
        surveyentity__entity__in=x, surveyentity__surveybreakdown__in=y,
        surveyentity__surveybreakdown__surveyinstance__profile__in=z).distinct()


def suvs2(request):
    if request is None:
        return Survey.objects.none()
    entities = permissionentitycheck(request)
    if request.GET.getlist('entity', '') == "":
        x = Entity.objects.all()
    else:
        x = request.GET.getlist('entity', '')
    return Survey.objects.filter(surveyentity__entity__in=entities).filter(surveyentity__entity__in=x).distinct()


def breaks(request):
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
    if request.GET.getlist('profile', '') == "":
        z = Profile.objects.all()
    else:
        z = request.GET.getlist('profile', '')
    return SurveyBreakdown.objects.filter(surveyentity__entity__in=entities,
                                          surveyinstance__profile__in=profilelist).filter(
        surveyentity__entity__in=x, surveyentity__survey__in=y,
        surveyentity__surveybreakdown__surveyinstance__profile__in=z).values_list('surveybreakdown_category', flat=True).distinct()


def profs(request):
    if request is None:
        return Profile.objects.none()
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
    if request.GET.getlist('entity', '') == "":
        z = Entity.objects.all()
    else:
        z = request.GET.getlist('entity', '')
    return Profile.objects.filter(id__in=profilelist,
                                  surveyinstance__surveybreakdown__surveyentity__entity__in=entities).filter(
        surveyinstance__surveybreakdown__surveyentity__survey__in=x,
        surveyinstance__surveybreakdown__surveyentity__surveybreakdown__in=y,
        surveyinstance__surveybreakdown__surveyentity__entity__in=z).distinct()


class SurveyFilter(django_filters.FilterSet):
    entity = filters.ModelMultipleChoiceFilter('surveybreakdown__surveyentity__entity', queryset=ents, label="Church",
                                               widget=CheckboxSelectMultiple)
    survey = filters.ModelMultipleChoiceFilter('surveybreakdown__surveyentity__survey', queryset=suvs, label="Survey",
                                               widget=CheckboxSelectMultiple)
    breakdown = filters.ModelMultipleChoiceFilter('surveybreakdown', queryset=breaks, label="Reminder Category",
                                                  widget=CheckboxSelectMultiple)
    profile = filters.ModelMultipleChoiceFilter('profile', queryset=profs, label="Profile",
                                                widget=CheckboxSelectMultiple)

    class Meta:
        model = SurveyInstance
        fields = '__all__'
        exclude = ['surveyentity', 'survey_start_date', 'survey_end_date', 'survey_instance_complete']


class AdminFilter(django_filters.FilterSet):
    entity = filters.ModelMultipleChoiceFilter('entity', queryset=ents2, label="Church", widget=CheckboxSelectMultiple)
    survey = filters.ModelMultipleChoiceFilter('survey', queryset=suvs2, label="Survey", widget=CheckboxSelectMultiple)

    class Meta:
        model = SurveyEntity
        fields = '__all__'
        exclude = []


class StatusFilter(django_filters.FilterSet):
    Status = filters.MultipleChoiceFilter(choices=[('Assigned', 'Assigned'), ('Unassigned', 'Unassigned'),
                                                   ('In Use', 'In Use')], widget=CheckboxSelectMultiple, label="Status")

    class Meta:
        model = SurveyEntity
        fields = '__all__'
        exclude = []