from django.shortcuts import render
from django.http import HttpResponse
from website.decorators import allowed_users
from data.models import *
from .filters import AnswerFilter, AnswerFilter2
from django.contrib.auth.decorators import login_required
from data.functions import permissionprofilecheck, permissionentitycheck
from django.db.models.functions import TruncMonth
from django.db.models import Sum
import pandas as pd
import numpy as np
from datetime import datetime
from django.core.paginator import Paginator
from itertools import chain


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def report(request):
    profilelist = permissionprofilecheck(request)
    entitylist = permissionentitycheck(request)

    if "?" in request.get_full_path():
        searched = 1
    else:
        searched = 0

    # ---#
    # Name shortcuts

    # this list gives the shortcts for the surveys and questions used.
    # If a survey name or question content is changed the following list will need to be updated.
    sun = 'Sunday Service Attendance'  # Survey
    sunadult = "How many adults aged 16+ attended this service?"  # Question as part of the sun survey
    sunchild = "How many children aged 0-15 attended this service?"  # Question as part of the sun survey
    sunonline = 'Sunday Service Online Views'  # Survey
    smg = 'Small Group Attendance'  # Survey
    serve = 'Volunteer Numbers'  # Survey
    alpha = 'Alpha Attendance'
    rgg = 'Rising Generation Attendance'
    stg = 'Social Transformation Participation'

    integerfilterlist = AnswerInteger.objects.filter(
        surveyinstance__surveybreakdown__surveyentity__entity__in=entitylist,
        surveyinstance__profile__in=profilelist).distinct()
    answerfilter = AnswerFilter(request.GET, request=request, queryset=integerfilterlist)
    answerfilterlist = answerfilter.qs





    # ---#
    # how many times a day apears in a month calculator

    # Sunday Service - number of days in a month generator
    sundaynumberofdates = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=sun).values_list(
        'surveyinstance__survey_date', flat=True)

    # converts all dates to be the first of the month
    sundaylist = []
    for x in sundaynumberofdates:
        y = x.replace(day=1)
        sundaylist.append(y)

    # creates a dictionary that ths the first day of the month and then the number of seperate occasions in that month
    sundaygroupdict = {}
    for c in range(len(sundaylist)):
        sundaygroupdict[sundaylist[c]] = sundaylist.count(sundaylist[c])
    sundaygrouptable = pd.DataFrame.from_dict(sundaygroupdict, orient='index', columns=['ssweeks'])




    # Rising Gen - number of days in a month generator
    risingnumberofdates = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=rgg).values_list(
        'surveyinstance__survey_date', flat=True)
    # converts all dates to be the first of the month
    risinglist = []
    for x in risingnumberofdates:
        y = x.replace(day=1)
        risinglist.append(y)
    # creates a dictionary that ths the first day of the month and then the number of seperate occasions in that month
    risinggroupdict = {}
    for c in range(len(risinglist)):
        risinggroupdict[risinglist[c]] = risinglist.count(risinglist[c])
    risinggrouptable = pd.DataFrame.from_dict(risinggroupdict, orient='index', columns=['rgweeks'])




    # Serving - number of days in a month generator
    servingnumberofdates = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=serve).values_list(
        'surveyinstance__survey_date', flat=True)
    # converts all dates to be the first of the month
    servinglist = []
    for x in servingnumberofdates:
        y = x.replace(day=1)
        servinglist.append(y)
    # creates a dictionary that ths the first day of the month and then the number of seperate occasions in that month
    servinggroupdict = {}
    for c in range(len(servinglist)):
        servinggroupdict[servinglist[c]] = servinglist.count(servinglist[c])
    servinggrouptable = pd.DataFrame.from_dict(servinggroupdict, orient='index', columns=['serveweeks'])




    # Social Transformation - number of days in a month generator
    stnumberofdates = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=serve).values_list(
        'surveyinstance__survey_date', flat=True)
    # converts all dates to be the first of the month
    stlist = []
    for x in stnumberofdates:
        y = x.replace(day=1)
        stlist.append(y)
    # creates a dictionary that ths the first day of the month and then the number of seperate occasions in that month
    stgroupdict = {}
    for c in range(len(stlist)):
        stgroupdict[stlist[c]] = stlist.count(stlist[c])
    stgrouptable = pd.DataFrame.from_dict(stgroupdict, orient='index', columns=['stweeks'])





    # Small Group - number of days in a month generator
    smallgroupnumberofdates = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=smg).values_list(
        'surveyinstance__survey_date', flat=True)
    # converts all dates to be the first of the month
    smallgrouplist = []
    for x in smallgroupnumberofdates:
        y = x.replace(day=1)
        smallgrouplist.append(y)
    # creates a dictionary that ths the first day of the month and then the number of seperate occasions in that month
    smallgroupdict = {}
    for c in range(len(smallgrouplist)):
        smallgroupdict[smallgrouplist[c]] = smallgrouplist.count(smallgrouplist[c])
    smallgrouptable = pd.DataFrame.from_dict(smallgroupdict, orient='index', columns=['sgweeks'])



    # Alpha - number of days in a month generator
    alphanumberofdates = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=alpha).values_list(
        'surveyinstance__survey_date', flat=True)
    # converts all dates to be the first of the month
    alphalist = []
    for x in alphanumberofdates:
        y = x.replace(day=1)
        alphalist.append(y)
    # creates a dictionary that ths the first day of the month and then the number of seperate occasions in that month
    alphadict = {}
    for c in range(len(alphalist)):
        alphadict[alphalist[c]] = alphalist.count(alphalist[c])
    alphatable = pd.DataFrame.from_dict(alphadict, orient='index', columns=['alpweeks'])



    # merges the different date count tables above into a single
    # table to be used to calculate averages in the summary table below
    monthstable = pd.merge(sundaygrouptable, smallgrouptable, how="outer", left_index=True, right_index=True)
    monthstable = pd.merge(monthstable, alphatable, how="outer", left_index=True, right_index=True)
    monthstable = pd.merge(monthstable, risinggrouptable, how="outer", left_index=True, right_index=True)
    monthstable = pd.merge(monthstable, servinggrouptable, how="outer", left_index=True, right_index=True)
    monthstable = pd.merge(monthstable, stgrouptable, how="outer", left_index=True, right_index=True)
    monthstable.reset_index(inplace=True)
    monthstable = monthstable.rename(columns={'index': 'month'})

    # --- #
    # Grouping of data from surveys into months

    # Sunday Service Totals
    sundaygroupedintegers = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=sun).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_integer'))  # Truncate to month and add to select list

    sundayadultgroupedintegers = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=sun).filter(
        question__question_content=sunadult).annotate(month=TruncMonth('surveyinstance__survey_date')).values(
        'month').annotate(averagess=Sum('answer_integer'))  # Truncate to month and add to select list

    sundaychildrengroupedintegers = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=sun).filter(
        question__question_content=sunchild).annotate(month=TruncMonth('surveyinstance__survey_date')).values(
        'month').annotate(averagess=Sum('answer_integer'))  # Truncate to month and add to select list

    # Sunday Online Totals
    sundayonlinegroupedintegers = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=sunonline).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_integer'))  # Truncate to month and add to select list

    # Serving totals
    servinggrouped = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=serve).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_integer'))  # Truncate to month and add to select list

    # Small Group totals
    smallgroupgrouped = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=smg).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_integer'))  # Truncate to month and add to select list

    # Rising Generation totals
    risinggengrouped = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=rgg).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_integer'))  # Truncate to month and add to select list

    # Small Group totals
    socialtransformationgrouped = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=stg).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_integer'))  # Truncate to month and add to select list

    # Alpha totals
    alphagrouped = answerfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=alpha).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_integer'))  # Truncate to month and add to select list


    # --- #
    # Data conversion into pandas tables

    # Sunday Service attendees
    # converting the combined attendees totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if sundaygroupedintegers.exists():
        for q in sundaygroupedintegers:
            sunday_service_attendance = pd.DataFrame.from_dict(sundaygroupedintegers)
            sunday_service_attendance.rename(columns={"averagess": "ssco"}, inplace=True)
    else:
        sunday_service_attendance = pd.DataFrame(columns=["month", "ssco"], data=[["", ""]])

    # Sunday Service Adult Attendees
    # converting the adult attendees totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if sundayadultgroupedintegers.exists():
        for q in sundayadultgroupedintegers:
            sunday_service_adult_attendance = pd.DataFrame.from_dict(sundayadultgroupedintegers)
            sunday_service_adult_attendance.rename(columns={"averagess": "ssa"}, inplace=True)
    else:
        sunday_service_adult_attendance = pd.DataFrame(columns=["month", "ssa"], data=[["", ""]])

    # Sunday Service Child Attendees
    # converting the child attendees totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if sundaychildrengroupedintegers.exists():
        for q in sundaychildrengroupedintegers:
            sunday_service_children_attendance = pd.DataFrame.from_dict(sundaychildrengroupedintegers)
            sunday_service_children_attendance.rename(columns={"averagess": "ssc"}, inplace=True)
    else:
        sunday_service_children_attendance = pd.DataFrame(columns=["month", "ssc"], data=[["", ""]])

    # Sunday Online Attendees
    # converting the online attendees totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if sundayonlinegroupedintegers.exists():
        for q in sundayonlinegroupedintegers:
            sunday_service_online_attendance = pd.DataFrame.from_dict(sundayonlinegroupedintegers)
            sunday_service_online_attendance.rename(columns={"averagess": "sso"}, inplace=True)
    else:
        sunday_service_online_attendance = pd.DataFrame(columns=["month", "sso"], data=[["", ""]])

    # Serving totals formed into pandas tables
    # converting the serving totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if servinggrouped.exists():
        for q in servinggrouped:
            serving_totals = pd.DataFrame.from_dict(servinggrouped)
            serving_totals.rename(columns={"averagess": "st"}, inplace=True)
    else:
        serving_totals = pd.DataFrame(columns=["month", "st"], data=[["", ""]])

    # Small Group totals formed into pandas tables
    # converting the small group totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if smallgroupgrouped.exists():
        for q in smallgroupgrouped:
            small_group_totals = pd.DataFrame.from_dict(smallgroupgrouped)
            small_group_totals.rename(columns={"averagess": "sgt"}, inplace=True)
    else:
        small_group_totals = pd.DataFrame(columns=["month", "sgt"], data=[["", ""]])

    # Alpha totals formed into pandas tables
    # converting the alpha totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if alphagrouped.exists():
        for q in alphagrouped:
            alpha_totals = pd.DataFrame.from_dict(alphagrouped)
            alpha_totals.rename(columns={"averagess": "alpt"}, inplace=True)
    else:
        alpha_totals = pd.DataFrame(columns=["month", "alpt"], data=[["", ""]])

    # Alpha totals formed into pandas tables
    # converting the alpha totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if risinggengrouped.exists():
        for q in risinggengrouped:
            risinggen_totals = pd.DataFrame.from_dict(risinggengrouped)
            risinggen_totals.rename(columns={"averagess": "rgt"}, inplace=True)
    else:
        risinggen_totals = pd.DataFrame(columns=["month", "rgt"], data=[["", ""]])

    # Alpha totals formed into pandas tables
    # converting the alpha totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if socialtransformationgrouped.exists():
        for q in socialtransformationgrouped:
            soctran_totals = pd.DataFrame.from_dict(socialtransformationgrouped)
            soctran_totals.rename(columns={"averagess": "stt"}, inplace=True)
    else:
        soctran_totals = pd.DataFrame(columns=["month", "stt"], data=[["", ""]])

    # --- #
    # Combining the individual tables into a summary

    # Creation of te Summary Combined Table
    table = pd.merge(sunday_service_attendance, sunday_service_adult_attendance, how="outer", on='month')
    table = pd.merge(table, sunday_service_children_attendance, how="outer", on='month')
    table = pd.merge(table, sunday_service_online_attendance, how="outer", on='month')
    table = pd.merge(table, alpha_totals, how="outer", on='month')
    table = pd.merge(table, small_group_totals, how="outer", on='month')
    table = pd.merge(table, serving_totals, how="outer", on='month')
    table = pd.merge(table, risinggen_totals, how="outer", on='month')
    table = pd.merge(table, soctran_totals, how="outer", on='month')
    table = pd.merge(table, monthstable, how="outer", on='month')
    table = table.rename(columns={'month': 'Month'})

    # Adding additional calculated columns to the summary table
    table['Sunday All Ages'] = table['ssco'] / table[
        'ssweeks']  # create an average attendance based on the total attendance divided by the sundays in the month
    table['Sunday Adults'] = table['ssa'] / table['ssweeks']  # Average Adult Attendance
    table['Sunday Children'] = table['ssc'] / table['ssweeks']  # Average Children Attendance
    table['Sunday Online'] = table['sso'] / table['ssweeks']  # Average online Attendance
    table['Alpha Attendance'] = table['alpt'] / table['alpweeks']  # Average online Attendance
    table['Small Groups'] = table['sgt'] / table['sgweeks']  # Average online Attendance
    table['Serving'] = table['st']/table['serveweeks']  # Average online Attendance
    table['Rising Generation'] = table['rgt']/table['rgweeks']  # Average online Attendance
    table['Social Transformation'] = table['stt']/table['stweeks']  # Average online Attendance

    #table['Total Giving'] = table['totalgiving']  # Average online Attendance

    # Cleaning up the summary table
    table = table.drop(
        ['ssweeks', 'sgt', 'alpweeks', 'sgweeks', 'rgweeks', 'serveweeks', 'stweeks', 'alpt', 'ssco', 'ssa', 'ssc', 'sso', 'st', 'stt', 'rgt'],
        axis=1)  # Remove the columns for full month totals for attendance and the number of sundays in the week

    # Clearing blank values and rows
    table.replace('', np.nan, inplace=True)  # All blanks are replaced by nan's
    table = table.dropna(how='all')  # any row that is all nans is removed
    table = table.replace(np.nan, '', regex=True)  # replace all empty values show as nan with true blanks
    # change the attendance rounded numbers totals to be integers

    # creating the data for the CSV file Download
    listolists = table.values.tolist()
    # create a version of the pandas table to be a list of lists for use with the csv creator
    headers = ['Month', 'Sunday All Ages', 'Sunday Adults',
               'Sunday Children', 'Sunday Online',
               'Alpha Attendance',
               'Small Groups', 'Serving','Rising Gen','Social']  # Headers for the csv file and for the pandas table
    time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")  # Timeand date stamp for the csv file name
    myFileName = f'attachment; filename=CRT_Impact_data_{time}.csv'  # csv file name creation


    # When the download file btton is clicked
    if request.method == "POST":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = myFileName
        table.to_csv(path_or_buf=response, float_format='%.2f', index=False, decimal=".", date_format='%Y-%m-%d')
        return response

    # rendering the view
    return render(request, "analytics/report.html",
                  {'table': table, 'headers': headers, 'listolists': listolists,
                   'answerfilter': answerfilter, 'searched': searched})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def givingreport(request):
    profilelist = permissionprofilecheck(request)
    entitylist = permissionentitycheck(request)

    if "?" in request.get_full_path():
        searched = 1
    else:
        searched = 0

    integerfilterlist = AnswerInteger.objects.filter(
        surveyinstance__surveybreakdown__surveyentity__entity__in=entitylist,
        surveyinstance__profile__in=profilelist).distinct()
    answerfilter = AnswerFilter(request.GET, request=request, queryset=integerfilterlist)
    answerfilterlist = answerfilter.qs
    integeranswers = answerfilterlist.all()

    floatfilterlist = AnswerFloat.objects.filter(
        surveyinstance__surveybreakdown__surveyentity__entity__in=entitylist,
        surveyinstance__profile__in=profilelist).distinct()
    answerfloatfilter = AnswerFilter(request.GET, request=request, queryset=floatfilterlist)
    answerfloatfilterlist = answerfloatfilter.qs
    floatanswers = answerfloatfilterlist.all()

    combinedanswers = list(chain(floatanswers, integeranswers))
    # ---#
    # Name shortcuts

    # this list gives the shortcts for the surveys and questions used.
    # If a survey name or question content is changed the following list will need to be updated.
    give = 'Giving and Income'  # Survey
    giveRGA = "What was your regular giving (Gift Aid eligible)?"  # Question as part of the give survey
    giveRNGA = "What was your regular giving (NOT Gift Aid eligible)?"  # Question as part of the give survey
    giveOOGA = "What was your one-off giving (Gift Aid eligible)?"  # Question as part of the give survey
    giveOONGA = "What was your one-off giving (NOT Gift Aid eligible)?"  # Question as part of the give survey
    giveGrant = "What was your total grant income?"
    giveOther = "What was your total other income?"  # Question as part of the give survey


    # ---#
    # how many times a day apears in a month calculator



    # Giving Totals
    givingregularGAgrouped = answerfloatfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=give).filter(
        question__question_content=giveRGA).annotate(month=TruncMonth('surveyinstance__survey_date')).values(
        'month').annotate(averagess=Sum('answer_float'))  # Truncate to month and add to select list

    givingregularNGAgrouped = answerfloatfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=give).filter(
        question__question_content=giveRNGA).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_float'))  # Truncate to month and add to select list

    givingoneoffGAgrouped = answerfloatfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=give).filter(
        question__question_content=giveOOGA).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_float'))  # Truncate to month and add to select list

    givingoneoffNGAgrouped = answerfloatfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=give).filter(
        question__question_content=giveOONGA).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_float'))  # Truncate to month and add to select list

    givingGrantgrouped = answerfloatfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=give).filter(
        question__question_content=giveGrant).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_float'))  # Truncate to month and add to select list

    givingOthergrouped = answerfloatfilterlist.filter(
        surveyinstance__surveybreakdown__surveyentity__survey__survey_name=give).filter(
        question__question_content=giveOther).annotate(
        month=TruncMonth('surveyinstance__survey_date')).values('month').annotate(
        averagess=Sum('answer_float'))  # Truncate to month and add to select list


    # --- #
    # Data conversion into pandas tables


    # Giving totals formed into pandas tables
    # converting the giving regular Gift Aid totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if givingregularGAgrouped.exists():
        for q in givingregularGAgrouped:
            giving_totalsRGA = pd.DataFrame.from_dict(givingregularGAgrouped)
            giving_totalsRGA.rename(columns={"averagess": "grga"}, inplace=True)
            giving_totalsRGA.insert(2, 'grgaadj', giving_totalsRGA['grga'] * 1.25)
    else:
        giving_totalsRGA = pd.DataFrame(columns=["month", "grga", "grgaadj"], data=[["", "", ""]])

    # converting the giving regular Non Gift Aid totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if givingregularNGAgrouped.exists():
        for q in givingregularNGAgrouped:
            giving_totalsRNGA = pd.DataFrame.from_dict(givingregularNGAgrouped)
            giving_totalsRNGA.rename(columns={"averagess": "grnga"}, inplace=True)
    else:
        giving_totalsRNGA = pd.DataFrame(columns=["month", "grnga"], data=[["", ""]])

    # converting the giving one off Gift Aid totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if givingoneoffGAgrouped.exists():
        for q in givingoneoffGAgrouped:
            giving_totalsOOGA = pd.DataFrame.from_dict(givingoneoffGAgrouped)
            giving_totalsOOGA.rename(columns={"averagess": "googa"}, inplace=True)
            giving_totalsOOGA.insert(2, 'googaadj', giving_totalsOOGA['googa'] * 1.25)
    else:
        giving_totalsOOGA = pd.DataFrame(columns=["month", "googa", "googaadj"], data=[["", "", ""]])

    # converting the giving one off non Gift Aid totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if givingoneoffNGAgrouped.exists():
        for q in givingoneoffNGAgrouped:
            giving_totalsOONGA = pd.DataFrame.from_dict(givingoneoffNGAgrouped)
            giving_totalsOONGA.rename(columns={"averagess": "goonga"}, inplace=True)
    else:
        giving_totalsOONGA = pd.DataFrame(columns=["month", "goonga"], data=[["", ""]])

    # converting the giving one off non Gift Aid totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if givingOthergrouped.exists():
        for q in givingOthergrouped:
            giving_totalsOther = pd.DataFrame.from_dict(givingOthergrouped)
            giving_totalsOther.rename(columns={"averagess": "gother"}, inplace=True)
    else:
        giving_totalsOther = pd.DataFrame(columns=["month", "gother"], data=[["", ""]])

    # converting the giving one off non Gift Aid totals into a pandas table.
    # if there is no data then it creates a blank table to avoid an error
    if givingGrantgrouped.exists():
        for q in givingGrantgrouped:
            giving_totalsGrant = pd.DataFrame.from_dict(givingGrantgrouped)
            giving_totalsGrant.rename(columns={"averagess": "ggrant"}, inplace=True)
    else:
        giving_totalsGrant = pd.DataFrame(columns=["month", "ggrant"], data=[["", ""]])


    # --- #
    # Combining the individual giving tables into a giving summary

    # Creation of the giving table
    givingtable = pd.merge(giving_totalsRGA, giving_totalsRNGA, how="outer",
                           on='month')  # merging the regular gift aid with the regular non gift aid to form the table
    givingtable = pd.merge(givingtable, giving_totalsOOGA, how="outer",
                           on='month')  # merging the table with the one off gift aid
    givingtable = pd.merge(givingtable, giving_totalsOONGA, how="outer",
                           on='month')  # merging the table with the one off non gift aid
    givingtable = pd.merge(givingtable, giving_totalsGrant, how="outer",
                           on='month')  # merging the table with the one off non gift aid
    givingtable = pd.merge(givingtable, giving_totalsOther, how="outer",
                           on='month')  # merging the table with the one off non gift aid
    givingtable.insert(9, 'totalgiving', (
                givingtable['grgaadj'] + givingtable['grnga'] + givingtable['googaadj'] + givingtable['goonga']
                + givingtable['gother'] + givingtable['ggrant']))
    # adding a new column to hold the totals of the calculated gift aid and non gift aid for regular and one off

    givingtable.columns = ['Month', 'Regular GA', 'Regular GA adjusted',
               'Regular no GA', 'One-off GA',
               'One-off GA adjusted',
               'One-off no GA', 'Grants', 'Other income', 'Total income']

    # Clearing blank values and rows
    givingtable.replace('', np.nan, inplace=True)  # All blanks are replaced by nan's
    givingtable = givingtable.dropna(how='all')  # any row that is all nans is removed
    givingtable = givingtable.replace(np.nan, '', regex=True)  # replace all empty values show as nan with true blanks

    # change the attendance rounded numbers totals to be integers

    # creating the data for the CSV file Download
    givinglistolists = givingtable.values.tolist()
    # create a version of the pandas table to be a list of lists for use with the csv creator
    headers = ['Month', 'Regular GA', 'Regular GA adjusted',
               'Regular no GA', 'One-off GA',
               'One-off GA adjusted',
               'One-off no GA', 'Grants', 'Other income', 'Total income',
               ]  # Headers for the csv file and for the pandas table
    time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")  # Timeand date stamp for the csv file name
    myFileName = f'attachment; filename=CRT_Impact_givingdata_{time}.csv'  # csv file name creation

    # When the download file btton is clicked
    if request.method == "POST":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = myFileName
        givingtable.to_csv(path_or_buf=response, float_format='%.2f', index=False, decimal=".", date_format='%Y-%m-%d')
        return response

    # rendering the view
    return render(request, "analytics/givingreport.html",
                  { 'combinedanswers': combinedanswers,
                   'answerfilter': answerfilter, 'searched': searched, 'givinglistolists': givinglistolists, 'headers': headers})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def allanswers(request):
    profilelist = permissionprofilecheck(request)
    entitylist = permissionentitycheck(request)

    if "?" in request.get_full_path():
        searched = 1
    else:
        searched = 0

    integerfilterlist = AnswerInteger.objects.filter(
        surveyinstance__surveybreakdown__surveyentity__entity__in=entitylist,
        surveyinstance__profile__in=profilelist).distinct()
    answerfilter = AnswerFilter2(request.GET, request=request, queryset=integerfilterlist)
    answerfilterlist = answerfilter.qs
    integeranswers = answerfilterlist.all()

    floatfilterlist = AnswerFloat.objects.filter(
        surveyinstance__surveybreakdown__surveyentity__entity__in=entitylist,
        surveyinstance__profile__in=profilelist).distinct()
    answerfloatfilter = AnswerFilter(request.GET, request=request, queryset=floatfilterlist)
    answerfloatfilterlist = answerfloatfilter.qs
    floatanswers = answerfloatfilterlist.all()

    combinedanswers = list(chain(floatanswers, integeranswers))

    return render(request, "analytics/allanswers.html",
                  { 'combinedanswers': combinedanswers,
                   'answerfilter': answerfilter, 'searched': searched})