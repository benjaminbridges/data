from dateutil import rrule as dr
from dateutil import relativedelta
from datetime import timedelta
from dateutil.relativedelta import *
from .forms import *
from .models import *


def dateinstances(start, survey_interval, occurances):
    dateslist = []

    if survey_interval == "Daily":
        rr = dr.rrule(dr.DAILY, dtstart=start, count=occurances)
        for d in rr:
            survey_due = [d.strftime('%Y-%m-%d')]
            survey_start_date = survey_due
            survey_end_date = survey_due
            dateslist.append([survey_due, survey_start_date, survey_end_date])

    elif survey_interval == "Daily weekdays":
        rr = dr.rrule(dr.DAILY, byweekday=(0, 1, 2, 3, 4), dtstart=start, count=occurances)
        for d in rr:
            survey_due = [d.strftime('%Y-%m-%d')]
            survey_start_date = survey_due
            survey_end_date = survey_due
            dateslist.append([survey_due, survey_start_date, survey_end_date])

    elif survey_interval == "Weekly":
        rr = dr.rrule(dr.WEEKLY, dtstart=start, count=occurances)
        for d in rr:
            survey_due = [d.strftime('%Y-%m-%d')]
            e = d - (timedelta(6))
            survey_start_date = [e.strftime('%Y-%m-%d')]
            survey_end_date = survey_due
            dateslist.append([survey_due, survey_start_date, survey_end_date])

    elif survey_interval == "Fortnightly":
        rr = dr.rrule(dr.WEEKLY, dtstart=start, interval=2, count=occurances)
        for d in rr:
            survey_due = [d.strftime('%Y-%m-%d')]
            e = d - (timedelta(13))
            survey_start_date = [e.strftime('%Y-%m-%d')]
            survey_end_date = survey_due
            dateslist.append([survey_due, survey_start_date, survey_end_date])

    elif survey_interval == "Monthly":
        rr = dr.rrule(dr.MONTHLY, dtstart=start, count=occurances)
        for d in rr:
            survey_due = [d.strftime('%Y-%m-%d')]
            e = d - relativedelta(months=+1) + (timedelta(1))
            survey_start_date = [e.strftime('%Y-%m-%d')]
            survey_end_date = survey_due
            dateslist.append([survey_due, survey_start_date, survey_end_date])

    elif survey_interval == "Last day of the month":
        rr = dr.rrule(dr.MONTHLY, dtstart=start, count=occurances, bymonthday=-1)
        for d in rr:
            survey_due = [d.strftime('%Y-%m-%d')]
            e = d.replace(day=1)
            survey_start_date = [e.strftime('%Y-%m-%d')]
            survey_end_date = survey_due
            dateslist.append([survey_due, survey_start_date, survey_end_date])

    elif survey_interval == "First Working Day Monthly":
        rr = dr.rrule(dr.MONTHLY, dtstart=start, byweekday=(0, 1, 2, 3, 4), bysetpos=1, count=occurances)
        for d in rr:
            survey_due = [d.strftime('%Y-%m-%d')]
            e = d - relativedelta(months=+1)
            f = e.replace(day=1)
            survey_start_date = [f.strftime('%Y-%m-%d')]
            g = d.replace(day=1)
            h = g - timedelta(days=1)
            survey_end_date = [h.strftime('%Y-%m-%d')]
            dateslist.append([survey_due, survey_start_date, survey_end_date])

    elif survey_interval == "Annually":
        rr = dr.rrule(dr.YEARLY, dtstart=start, count=occurances)
        for d in rr:
            survey_due = [d.strftime('%Y-%m-%d')]
            e = d - relativedelta(years=+1) + (timedelta(1))
            survey_start_date = [e.strftime('%Y-%m-%d')]
            survey_end_date = survey_due
            dateslist.append([survey_due, survey_start_date, survey_end_date])

    elif survey_interval == "Previous Year":
        rr = dr.rrule(dr.YEARLY, dtstart=start, count=occurances)
        for d in rr:
            survey_due = [d.strftime('%Y-%m-%d')]
            e = d - relativedelta(years=+1)
            f = e.replace(day=1, month=1)
            survey_start_date = [f.strftime('%Y-%m-%d')]
            g = d - relativedelta(years=+1)
            h = e.replace(day=31, month=12)
            survey_end_date = [h.strftime('%Y-%m-%d')]
            dateslist.append([survey_due, survey_start_date, survey_end_date])

    return dateslist


# --- #
# --- #
# --- #

def answerselection(request, questiontype, choice):
    if questiontype == 'Short Text':
        type = AnswerShortText
        form = ShortTextAnswerForm(request.POST)
    elif questiontype == 'Long Text':
        type = AnswerLongText
        form = LongTextAnswerForm(request.POST)
    elif questiontype == 'File':
        type = AnswerFile
        form = FileAnswerForm(request.POST)
    elif questiontype == 'Whole Number':
        type = AnswerInteger
        form = IntegerAnswerForm(request.POST)
    elif questiontype == 'Decimal Number':
        type = AnswerFloat
        form = FloatAnswerForm(request.POST)
    # elif questiontype == 'Duration':
    #  type = AnswerDuration
    #  form = DurationAnswerForm(request.POST)
    # elif questiontype == 'Money':
    #  type = AnswerCurrency
    #  form = MoneyAnswerForm(request.POST)
    elif questiontype == 'Date':
        type = AnswerDate
        form = DateAnswerForm(request.POST)
    if choice == 'type':
        return type
    elif choice == 'form':
        return form


# def permissions(user):
#  if user__profile__site_permission ==

def permissionentitycheck(request):
    profilepermission = Profile.objects.values_list('site_permission', flat=True).get(user=request.user)

    entitylistids = Profile.objects.values_list('entity', flat=True).filter(user=request.user)
    entitylist = Entity.objects.filter(id__in=entitylistids)
    orglist = Organisation.objects.filter(entity__in=entitylistids)
    orgentitylist = Entity.objects.filter(org__in=orglist)
    allentitylist = Entity.objects.all()

    if profilepermission == 'entity':
        return entitylist
    elif profilepermission == 'org':
        return orgentitylist
    else:
        return allentitylist


def permissionprofilecheck(request):
    profilepermission = Profile.objects.values_list('site_permission', flat=True).get(user=request.user)

    myprofile = Profile.objects.filter(user=request.user)

    allprofiles = Profile.objects.all()

    if profilepermission == 'user':
        return myprofile
    else:
        return allprofiles


# Answer Breakdowns

def surveyentityanswers():
    surveyentityanswerlist = []
    surveyentityanswerlist.extend(
        AnswerInteger.objects.values_list('surveyinstance__surveybreakdown__surveyentity', flat=True).distinct())
    surveyentityanswerlist.extend(
        AnswerDate.objects.values_list('surveyinstance__surveybreakdown__surveyentity', flat=True).distinct())
    surveyentityanswerlist.extend(
        AnswerFile.objects.values_list('surveyinstance__surveybreakdown__surveyentity', flat=True).distinct())
    surveyentityanswerlist.extend(
        AnswerFloat.objects.values_list('surveyinstance__surveybreakdown__surveyentity', flat=True).distinct())
    surveyentityanswerlist.extend(
        AnswerCurrency.objects.values_list('surveyinstance__surveybreakdown__surveyentity', flat=True).distinct())
    surveyentityanswerlist.extend(
        AnswerDuration.objects.values_list('surveyinstance__surveybreakdown__surveyentity', flat=True).distinct())
    surveyentityanswerlist.extend(
        AnswerLongText.objects.values_list('surveyinstance__surveybreakdown__surveyentity', flat=True).distinct())
    surveyentityanswerlist.extend(
        AnswerShortText.objects.values_list('surveyinstance__surveybreakdown__surveyentity', flat=True).distinct())
    return surveyentityanswerlist


# creates a list of all of the instances where an answer is ascociated.
def breakdownanswers(bdid):
    breakdownanswerlist = []
    breakdownanswerlist.extend(AnswerInteger.objects.values_list('surveyinstance', flat=True).filter(
        surveyinstance__surveybreakdown_id=bdid).distinct())
    breakdownanswerlist.extend(AnswerDate.objects.values_list('surveyinstance', flat=True).filter(
        surveyinstance__surveybreakdown_id=bdid).distinct())
    breakdownanswerlist.extend(AnswerFile.objects.values_list('surveyinstance', flat=True).filter(
        surveyinstance__surveybreakdown_id=bdid).distinct())
    breakdownanswerlist.extend(AnswerFloat.objects.values_list('surveyinstance', flat=True).filter(
        surveyinstance__surveybreakdown_id=bdid).distinct())
    breakdownanswerlist.extend(AnswerCurrency.objects.values_list('surveyinstance', flat=True).filter(
        surveyinstance__surveybreakdown_id=bdid).distinct())
    breakdownanswerlist.extend(AnswerDuration.objects.values_list('surveyinstance', flat=True).filter(
        surveyinstance__surveybreakdown_id=bdid).distinct())
    breakdownanswerlist.extend(AnswerLongText.objects.values_list('surveyinstance', flat=True).filter(
        surveyinstance__surveybreakdown_id=bdid).distinct())
    breakdownanswerlist.extend(AnswerShortText.objects.values_list('surveyinstance', flat=True).filter(
        surveyinstance__surveybreakdown_id=bdid).distinct())
    return breakdownanswerlist


def breakdowndelete(bdid):
    # create a list to hold the ids of all instances ascociated with this breakdown that have answers ascociated with them
    answeredlist = []
    answeredlist.extend(SurveyInstance.objects.values_list('id', flat=True).filter(id__in=breakdownanswers(bdid)))
    # if there are no answers then we can delete the breakdown and let cascade do its work.
    if len(answeredlist) == 0:
        SurveyBreakdown.objects.filter(id=bdid).delete()
    # but if there are answers then:
    else:
        # create a list to hold the ids of all instances ascociated with this breakdown
        allinstancelist = []
        allinstancelist.extend(SurveyInstance.objects.values_list('id', flat=True).filter(surveybreakdown=bdid))
        # cfor each item in the all list remove the item if there is the same item in the answered list, therefore getting a list of only the items without answers
        for item in answeredlist:
            allinstancelist.remove(item)
        # for all the filtered items without answers delete that instance
        for item in allinstancelist:
            SurveyInstance.objects.filter(id=item).delete()
        # then for all items with answers close the instance
        for item in answeredlist:
            SurveyInstance.objects.filter(id=item).update(surveyinstance_active=False)
        # then make the breakdown inactive
        SurveyBreakdown.objects.filter(id=bdid).update(surveybreakdown_active=False)


def breakdownuserdelete(pid, bdid):
    # create a list to hold the ids of all instances ascociated with this breakdown that have answers ascociated with them
    answeredlist = []
    answeredlist.extend(
        SurveyInstance.objects.values_list('id', flat=True).filter(id__in=breakdownanswers(bdid), profile=pid))
    # create a list to hold the ids of all instances ascociated with this breakdown
    allinstancelist = []
    allinstancelist.extend(
        SurveyInstance.objects.values_list('id', flat=True).filter(surveybreakdown=bdid, profile=pid))

    if len(answeredlist) == 0:
        SurveyInstance.objects.filter(id__in=allinstancelist).delete()
        SurveyBreakdownProfile.objects.filter(profile=pid, surveybreakdown=bdid).delete()
    # cfor each item in the all list remove the item if there is the same item in the answered list, therefore getting a list of only the items without answers
    else:
        for item in answeredlist:
            allinstancelist.remove(item)
        # for all the filtered items without answers delete that instance
        for item in allinstancelist:
            SurveyInstance.objects.filter(id=item).delete()
            # then for all items with answers close the instance
        for item in answeredlist:
            a = SurveyInstance.objects.filter(id=item).update(surveyinstance_active=False)
            b = SurveyBreakdownProfile.objects.filter(profile=pid, surveybreakdown__surveyinstance=item).update(
                surveybreakdownprofile_active=False)
    # then make the breakdown inactive
