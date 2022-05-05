from .functions import *
from .filters import *
from django.contrib import messages
from website.forms import *
from django.db.models import CharField, Value
from website.decorators import allowed_users
from data.functions import dateinstances
from datetime import timedelta, date, datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa'])
def orglist(request):
    return render(request, "data/orglist.html",
                  {"orgs": Organisation.objects.all()})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa'])
def orgdetail(request, id):
    org = get_object_or_404(Organisation, pk=id)
    entitys = Entity.objects.filter(org_id=id)
    return render(request, "data/orgdetail.html", {"org": org, "entitys": entitys})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa'])
def orgnew(request):
    if request.method == "POST":
        form = OrgForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            messages.success(request, data.org_name + 'has been set up')
            return redirect("orglist")
    else:
        form = OrgForm()
    return render(request, "data/orgnew.html", {"form": form})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa'])
def orgedit(request, oid):
    org = get_object_or_404(Organisation, pk=oid)
    if request.method == "POST":
        form = OrgEditForm(request.POST, request.FILES, instance=org)
        if form.is_valid():
            data = form.save()
            messages.success(request, data.org_name + 'has been updated')
            return redirect("orglist")
    else:
        form = OrgEditForm(instance=org)
    return render(request, "data/orgedit.html", {"form": form, 'org': org})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity'])
def entitylist(request):
    entitys = permissionentitycheck(request)
    return render(request, "data/entitylist.html",
                  {"entitys": entitys})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def entitydetail(request, id):
    entity = get_object_or_404(Entity, pk=id)
    suv = SurveyEntity.objects.values_list('survey_id', flat=True, ).filter(entity_id=id)
    surveys = Survey.objects.filter(id__in=suv)
    return render(request, "data/entitydetail.html", {"entity": entity, "surveys": surveys})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def entitynew(request):
    if request.method == "POST":
        form = EntityForm(request.POST)
        if form.is_valid():
            data = form.save()
            messages.success(request, data.entity_name + 'has been set up')
            return redirect("entitylist")
    else:
        form = EntityForm()
    return render(request, "data/entitynew.html", {"form": form})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def entityedit(request, eid):
    entity = get_object_or_404(Entity, pk=eid)
    if request.method == "POST":
        form = EntityEditForm(request.POST, instance=entity)
        if form.is_valid():
            data = form.save()
            messages.success(request, data.entity_name + 'has been updated')
            return redirect("entitylist")
    else:
        form = EntityEditForm(instance=entity)
    return render(request, "data/entityedit.html", {"form": form, 'entity': entity})

# Users


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def userlist(request):
    entitys = permissionentitycheck(request)
    users = Profile.objects.filter(entity__in=entitys).distinct().order_by('first_name')
    return render(request, "data/userlist.html",
                  {"entitys": entitys, 'users': users})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def userdetail(request, id):
    user = get_object_or_404(Profile, pk=id)
    entitys = permissionentitycheck(request)

    return render(request, "data/userdetail.html", {"user": user, "entitys": entitys})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def usernew(request):
    entities = permissionentitycheck(request)
    if request.method == "POST":
        form = ProfileForm(entities, request.POST)
        permission = request.POST['permission']
        if form.is_valid():
            form.save()
            obj = form.save(commit=False)
            obj.site_permission = permission
            obj.save()
            user = User.objects.get(username=obj.email)
            obj.user = user
            obj.save()
            messages.success(request, obj.user_name + 'has been added and an email has been sent inviting them to set up a password')
        return redirect("userlist")

    else:
        form = ProfileForm(entities)
    context = {'form': form}
    return render(request, 'data/usernew.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def useredit(request, id):
    user = get_object_or_404(Profile, pk=id)
    entities = permissionentitycheck(request)  # used in the SurveyForm to filter the choices for entities

    if request.method == "POST":
        form = ProfileEditForm(entities, request.POST, instance=user)
        permission = request.POST['permission']

        if form.is_valid():
            obj = form.save(commit=False)
            obj.site_permission = permission
            obj.save()
            messages.success(request,obj.user_name + 'has been updated')
        return redirect("userlist")

    else:
        form = ProfileEditForm(entities, instance=user)
    return render(request, "data/useredit.html", {"form": form, 'user': user})


# Surveys


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def surveylist(request):

    entitylist = permissionentitycheck(request)

    ininstance = SurveyInstance.objects.values_list('surveybreakdown__surveyentity__survey', flat=True)
    assigned = Survey.objects.all().filter(id__in=ininstance).filter(survey_active=True).filter(
        entity__in=entitylist).distinct()
    unassigned = Survey.objects.all().exclude(id__in=ininstance).filter(survey_active=True).filter(
        entity__in=entitylist).distinct()
    closed = Survey.objects.all().filter(survey_active=False).filter(entity__in=entitylist).distinct()
    createdbyuser = Survey.objects.all().filter(survey_created_by=request.user.profile).exclude(
        id__in=assigned).exclude(id__in=unassigned).exclude(id__in=closed).distinct()

    if unassigned.count == 0 and assigned.count == 0 and createdbyuser.count == 0 and closed.count == 0:
        nosurveys = True
    else:
        nosurveys = False

    return render(request, "data/surveylist.html",
                  {"assigned": assigned, "unassigned": unassigned, "closed": closed, 'createdbyuser': createdbyuser,
                   'nosurveys': nosurveys})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def surveydetail(request, sid):
    survey = get_object_or_404(Survey, pk=sid)
    itemexists = SurveyInstance.objects.filter(surveybreakdown__surveyentity__survey=sid).exists()
    ents = SurveyEntity.objects.values_list('entity_id', flat=True, ).filter(survey_id=sid)
    entitys = Entity.objects.filter(id__in=ents)
    questions = Question.objects.filter(survey=sid)
    breakdowncategorys = BreakdownCategory.objects.filter(survey=sid)
    return render(request, "data/surveydetail.html", {"survey": survey, "entitys": entitys, "questions": questions,
                                                      "breakdowncategorys": breakdowncategorys,
                                                      "itemexists": itemexists})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def surveynew(request):
    entities = permissionentitycheck(request)  # used in the SurveyForm to filter the choices for entities
    if request.method == "POST":
        form = SurveyForm(entities, request.POST)
        # the entities is passed in and this is used to filter the results based on who is logged in
        if form.is_valid():
            data = form.save(commit=False)
            data.survey_created_by = request.user.profile
            form.save()
            if form.cleaned_data.get('survey_entity_to_set_times') == True:
                return redirect("questionnew", data.id)
            else:
                return redirect("surveycentaltimes", data.id)
    else:
        form = SurveyForm(entities)
        # the entities is passed in and this is used to filter the results based on who is logged in

    return render(request, "data/surveynew.html", {"form": form})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def surveyedit(request, id):
    survey = get_object_or_404(Survey, pk=id)
    entities = permissionentitycheck(request)  # used in the SurveyForm to filter the choices for entities
    questions = Question.objects.filter(survey_id=id)
    if request.method == "POST":
        form = SurveyForm(entities, request.POST, instance=survey)
        if form.is_valid():
            data = form.save()
            messages.success(request, 'The "' + survey.survey_name + '" survey has been updated')
            if survey.survey_entity_to_set_times == True:
                return redirect('surveydetail', id)
            else:
                return redirect("surveycentaltimesedit", data.id)
    else:
        form = SurveyForm(entities, instance=survey)
    return render(request, "data/surveyedit.html", {"form": form, "questions": questions, 'survey': survey})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def surveyaddentity(request, sid):
    survey = get_object_or_404(Survey, pk=sid)
    allentities = Entity.objects.all()
    usedentities = Entity.objects.filter(survey=sid)
    filteredentities = allentities.exclude(id__in=usedentities)

    if request.method == "POST":
        form = SurveyAddEntitiesForm(filteredentities, request.POST, instance=survey)
        if form.is_valid():
            entities = form.cleaned_data.get('entity')
            for entity in entities:
                x = SurveyEntity.objects.create(entity=entity, survey=survey, survey_interval=survey.survey_interval,
                                                survey_occurances=survey.survey_occurances,
                                                survey_start_date=survey.survey_start_date)
                x.save()
            messages.success(request, 'Churches have been added to' + survey.survey_name )
            return redirect("surveydetail", survey.id)
    else:
        form = SurveyAddEntitiesForm(filteredentities, instance=survey)
    return render(request, "data/surveyaddentity.html", {"form": form, "survey": survey})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa'])
def surveydelete(request, sid):
    survey = get_object_or_404(Survey, pk=sid)
    if request.method == "POST":
        survey.delete()
        messages.success(request, 'The ' + survey.survey_name + ' survey has been deleted')
        return redirect("surveylist")
    return render(request, "data/surveydelete.html", {"survey": survey})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa'])
def surveyclose(request, sid):
    survey = get_object_or_404(Survey, pk=sid)
    if request.method == "POST":
        survey.survey_active = False
        survey.save()
        messages.success(request,
                         'The ' + survey.survey_name + ' survey has been closed. Survey Instances will no longer be '
                                                       'available but data collected has not been deleted')

        return redirect("surveylist")
    return render(request, "data/surveyclose.html", {"survey": survey})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def surveyadmin(request):

    entitylist = permissionentitycheck(request)

    if "?" in request.get_full_path():
        searched = 1
    else:
        searched = 0

    mysurveysset = SurveyEntity.objects.all()
    surveyfilter = AdminFilter(request.GET, request=request, queryset=mysurveysset)
    mysurveysset = surveyfilter.qs

    inuse = mysurveysset.filter(id__in=surveyentityanswers(), survey__survey_active=True).annotate(
        Status=Value('In Use', output_field=CharField()))
    unassigned = mysurveysset.filter(survey_times_assigned=False, entity__in=entitylist,
                                     survey__survey_active=True).exclude(id__in=inuse).annotate(
        Status=Value('Unassigned', output_field=CharField()))
    assigned = mysurveysset.filter(survey_times_assigned=True, entity__in=entitylist,
                                   survey__survey_active=True).exclude(id__in=inuse).annotate(
        Status=Value('Assigned', output_field=CharField()))

    inuse2 = StatusFilter(request.GET, queryset=inuse)
    inuse2b = inuse2.qs

    unassigned2 = StatusFilter(request.GET, queryset=unassigned)
    unassigned2b = unassigned2.qs

    assigned2 = StatusFilter(request.GET, queryset=assigned)
    assigned2b = assigned2.qs

    return render(request, "data/surveyadmin.html",
                  {"surveyentities": SurveyEntity.objects.all(), 'surveyfilter': surveyfilter, 'inuse2': inuse2,
                   'unassigned2': unassigned2, 'assigned2': assigned2, 'mysurveysset': mysurveysset,
                   'searched': searched, 'inuse': inuse2b, 'unassigned': unassigned2b, 'assigned': assigned2b})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def mysurveys(request):
    today = date.today()
    upcoming = date.today()+timedelta(14)

    profilelist = permissionprofilecheck(request)
    entitylist = permissionentitycheck(request)

    if "?" in request.get_full_path():
        searched = 1
    else:
        searched = 0

    loggedinuser = Profile.objects.values_list('id', flat=True).get(user=request.user)
    mysurveysset = SurveyInstance.objects.filter(profile__id=loggedinuser)
    surveyfilter = SurveyFilter(request.GET, request=request, queryset=mysurveysset)
    mysurveysset = surveyfilter.qs
    overduesurveys = mysurveysset.filter(survey_date__lt=today, survey_instance_complete=False, profile__in=profilelist,
                                         surveybreakdown__surveyentity__entity__in=entitylist).order_by('survey_date')
    upcomingsurveys = mysurveysset.filter(survey_date__gt=today, survey_date__lte=upcoming,
                                          survey_instance_complete=False, profile__id=loggedinuser).order_by(
        'survey_date')
    completedsurveys = mysurveysset.filter(survey_instance_complete=True, profile__id=loggedinuser).order_by(
        'survey_date').reverse()

    if overduesurveys.count == 0 and upcomingsurveys.count == 0 and completedsurveys.count == 0:
        nosurveys = True
    else:
        nosurveys = False

    return render(request, "data/mysurveys.html",
                  {"overduesurveys": overduesurveys, "upcomingsurveys": upcomingsurveys, 'searched': searched,
                   'nosurveys': nosurveys, "completedsurveys": completedsurveys, 'surveyfilter': surveyfilter})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def allsurveys(request):
    today = date.today()
    upcoming = date.today()+timedelta(14)

    if "?" in request.get_full_path():
        searched = 1
    else:
        searched = 0

    mysurveysset = SurveyInstance.objects.all()
    surveyfilter = SurveyFilter(request.GET, request=request, queryset=mysurveysset)
    mysurveysset = surveyfilter.qs
    # we use the pfofile list and entitylist to filter all the stuff in the tables by entity and by user
    entitylist = permissionentitycheck(request)

    overduesurveys = mysurveysset.filter(survey_date__lt=today, survey_instance_complete=False,
                                         surveybreakdown__surveyentity__entity__in=entitylist).order_by('survey_date')
    upcomingsurveys = mysurveysset.filter(survey_date__gt=today, survey_date__lte=upcoming,
                                          survey_instance_complete=False,
                                          surveybreakdown__surveyentity__entity__in=entitylist).order_by('survey_date')
    completedsurveys = mysurveysset.filter(survey_instance_complete=True,
                                           surveybreakdown__surveyentity__entity__in=entitylist).order_by(
        'survey_date').reverse()

    if overduesurveys.count == 0 and upcomingsurveys.count == 0 and completedsurveys.count == 0:
        nosurveys = True
    else:
        nosurveys = False

    return render(request, "data/allsurveys.html",
                  {"overduesurveys": overduesurveys, "upcomingsurveys": upcomingsurveys, 'searched': searched,
                   'nosurveys': nosurveys, "completedsurveys": completedsurveys, 'surveyfilter': surveyfilter})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def questionnew(request, id):
    survey = get_object_or_404(Survey, pk=id)
    entities = Entity.objects.filter(survey=survey)
    questions = Question.objects.filter(survey_id=id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.survey_id = id
            obj.save()
            return redirect("questionnew", id)
    else:
        form = QuestionForm()
    return render(request, "data/questionnew.html",
                  {"form": form, "survey": survey, "questions": questions, 'entities': entities})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def questionadd(request, id):
    survey = get_object_or_404(Survey, pk=id)
    entities = Entity.objects.filter(survey=survey)
    questions = Question.objects.filter(survey_id=id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.survey_id = id
            obj.save()
            return redirect("questionadd", id)
    else:
        form = QuestionForm()
    return render(request, "data/questionadd.html",
                  {"form": form, "survey": survey, "questions": questions, 'entities': entities})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def questionedit(request, sid, qid):
    survey = get_object_or_404(Survey, pk=sid)
    question = Question.objects.get(pk=qid)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'The "' + survey.survey_name + '" survey has been updated')
            return redirect("surveydetail", sid)
    else:
        form = QuestionForm(instance=question)
    return render(request, "data/questionedit.html", {"form": form, "survey": survey, "question": question})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def questiondelete(request, sid, qid):
    survey = get_object_or_404(Survey, pk=sid)
    question = Question.objects.get(pk=qid)
    if request.method == "POST":
        question.delete()
        messages.success(request,
                         'The question "' + question.question_content + '" has been removed from the "'
                         + survey.survey_name + '" survey')
        return redirect("surveydetail", sid)
    return render(request, "data/questiondelete.html", {"survey": survey, "question": question})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def breakdowncategorynew(request, id):
    survey = get_object_or_404(Survey, pk=id)
    entities = Entity.objects.filter(survey=survey)
    breakdowncategorys = BreakdownCategory.objects.filter(survey_id=id)
    if request.method == "POST":
        form = BreakdownCategoryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.survey_id = id
            obj.save()
            return redirect("breakdowncategorynew", id)
    else:
        form = BreakdownCategoryForm()
    return render(request, "data/breakdowncategorynew.html",
                  {"form": form, "survey": survey, "breakdowncategorys": breakdowncategorys, 'entities': entities})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def breakdowncategoryadd(request, id):
    survey = get_object_or_404(Survey, pk=id)
    entities = Entity.objects.filter(survey=survey)
    breakdowncategorys = BreakdownCategory.objects.filter(survey_id=id)
    if request.method == "POST":
        form = BreakdownCategoryForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.survey_id = id
            obj.save()
            return redirect("breakdowncategoryadd", id)
    else:
        form = BreakdownCategoryForm()
    return render(request, "data/breakdowncategoryadd.html",
                  {"form": form, "survey": survey, "breakdowncategorys": breakdowncategorys, 'entities': entities})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def breakdowncategoryedit(request, sid, bcid):
    survey = get_object_or_404(Survey, pk=sid)
    breakdowncategory = BreakdownCategory.objects.get(pk=bcid)
    if request.method == "POST":
        form = BreakdownCategoryForm(request.POST, instance=breakdowncategory)
        if form.is_valid():
            form.save()
            messages.success(request, 'The "' + breakdowncategory.category + '" has been edited from the "'
                         + survey.survey_name + '" survey')
            return redirect("surveydetail", sid)
    else:
        form = BreakdownCategoryForm(instance=breakdowncategory)
    return render(request, "data/breakdowncategoryedit.html",
                  {"form": form, "survey": survey, "breakdowncategory": breakdowncategory})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def breakdowncategorydelete(request, sid, bcid):
    survey = get_object_or_404(Survey, pk=sid)
    breakdowncategory = BreakdownCategory.objects.get(pk=bcid)
    if request.method == "POST":
        breakdowncategory.delete()
        messages.success(request,
                         'The question "' + breakdowncategory.category + '" has been removed from the "'
                         + survey.survey_name + '" survey')
        return redirect("surveydetail", sid)
    return render(request, "data/breakdowncategorydelete.html",
                  {"survey": survey, "breakdowncategory": breakdowncategory})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def surveycentaltimes(request, id):
    survey = get_object_or_404(Survey, pk=id)
    entities = Entity.objects.filter(survey=survey)
    entids = SurveyEntity.objects.filter(survey=survey)
    if request.method == "POST":
        form = FormSurveyDatesInitial(request.POST, instance=survey)
        if form.is_valid():
            data = form.save()
            for item in entids:
                item.survey_start_date = survey.survey_start_date
                item.survey_interval = survey.survey_interval
                item.survey_occurances = survey.survey_occurances
                item.save()
            return redirect("questionnew", data.id)
    else:
        form = FormSurveyDatesInitial(instance=survey)
    return render(request, "data/surveycentraltimes.html", {"form": form, 'survey': survey, 'entities': entities})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'centralteam'])
def surveycentaltimesedit(request, id):
    survey = get_object_or_404(Survey, pk=id)
    entities = Entity.objects.filter(survey=survey)
    entids = SurveyEntity.objects.filter(survey=survey)
    if request.method == "POST":
        form = FormSurveyDatesInitial(request.POST, instance=survey)
        if form.is_valid():
            data = form.save()
            for item in entids:
                item.survey_start_date = survey.survey_start_date
                item.survey_interval = survey.survey_interval
                item.survey_occurances = survey.survey_occurances
                item.save()
            messages.success(request, 'The ' + survey.survey_name + ' survey has been updated')
            return redirect("surveydetail", data.id)
        else:
            return redirect("index")
    else:
        form = FormSurveyDatesInitial(instance=survey)
    return render(request, "data/surveycentraltimesedit.html", {"form": form, 'survey': survey, 'entities': entities})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def surveybreakdown(request, sid, eid, seid):
    surveyentity = get_object_or_404(SurveyEntity, pk=seid)
    survey = get_object_or_404(Survey, pk=sid)
    entity = get_object_or_404(Entity, pk=eid)
    users = Profile.objects.filter(entity__id=eid)
    breakdowns = SurveyBreakdown.objects.filter(surveyentity_id=seid)
    breakdowncategorys = BreakdownCategory.objects.filter(survey=sid)
    breakdowncount = SurveyBreakdown.objects.filter(surveyentity_id=seid).count()
    questions = Question.objects.filter(survey_id=sid)
    profiles = Profile.objects.all()

    if survey.survey_interval != 'Weekly':
        reminderdays = [survey.survey_start_date]
    else:
        precedingweek = survey.survey_start_date - relativedelta(days=6)
        reminderdays = []
        for x in range(7):
            y = precedingweek + relativedelta(days=x)
            reminderdays.append(y)

    if request.method == "POST":
        form = BreakdownForm(users, request.POST)
        category = request.POST['category']
        reminder = request.POST['reminder']
        reminder = datetime.strptime(reminder, "%b. %d, %Y").date()

        gap = survey.survey_start_date - reminder
        gap = gap.days

        if form.is_valid():
            obj = form.save(commit=False)
            obj.surveyentity_id = seid
            obj.surveybreakdown_category = category
            obj.surveybreakdown_reminder_date = gap
            obj.save()
            form.save_m2m()
            return redirect("surveybreakdown", sid, eid, seid)
    else:
        form = BreakdownForm(users)
    return render(request, "data/surveybreakdown.html",
                  {"surveyentity": surveyentity, "form": form, "survey": survey, "breakdowns": breakdowns,
                   'entity': entity, 'profiles': profiles, 'breakdowncount': breakdowncount, 'questions': questions,
                   'breakdowncategorys': breakdowncategorys, 'reminderdays': reminderdays})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def surveybreakdowndelete(request, bdid, sid, eid, seid):
    survey = get_object_or_404(Survey, pk=sid)
    if request.method == "POST":
        breakdowndelete(bdid)
        messages.success(request,
                         'The reminder has been removed from the "'
                         + survey.survey_name + '" survey')
        return redirect("surveybreakdownedit", sid, eid, seid)
    return render(request, "data/surveybreakdowndelete.html", {'bdid': bdid, 'sid': sid, 'eid': eid, 'seid': seid})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def surveybreakdownedit(request, sid, eid, seid):
    surveyentity = get_object_or_404(SurveyEntity, pk=seid)
    survey = get_object_or_404(Survey, pk=sid)
    entity = get_object_or_404(Entity, pk=eid)
    breakdowns = SurveyBreakdown.objects.filter(surveyentity_id=seid).filter(surveybreakdown_active=True)
    users = Profile.objects.filter(entity__id=eid)
    breakdowncategorys = BreakdownCategory.objects.filter(survey=sid)
    breakdowncount = SurveyBreakdown.objects.filter(surveyentity_id=seid).filter(surveybreakdown_active=True).count()
    questions = Question.objects.filter(survey_id=sid)
    profiles = Profile.objects.all()
    breakdownprofilesactive = SurveyBreakdownProfile.objects.filter(surveybreakdown__in=breakdowns,
                                                                    surveybreakdownprofile_active=True)
    if request.method == "POST":
        form = BreakdownForm(users, request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.surveyentity_id = seid
            obj.save()
            form.save_m2m()
            messages.success(request, 'The ' + survey.survey_name + ' survey has been updated')
            return redirect("surveybreakdownedit", sid, eid, seid)
    else:
        form = BreakdownForm(users)
    return render(request, "data/surveybreakdownedit.html",
                  {"surveyentity": surveyentity, "form": form, "survey": survey, "breakdowns": breakdowns,
                   'entity': entity, 'profiles': profiles, 'breakdowncount': breakdowncount, 'questions': questions,
                   'breakdownprofilesactive': breakdownprofilesactive, 'breakdowncategorys': breakdowncategorys})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def surveybreakdownadd(request, sid, eid, seid):
    surveyentity = SurveyEntity.objects.get(pk=seid)
    survey = get_object_or_404(Survey, pk=sid)
    users = Profile.objects.filter(entity__id=eid)
    breakdowncategorys = BreakdownCategory.objects.filter(survey=sid)

    if survey.survey_interval != 'Weekly':
        reminderdays = [survey.survey_start_date]
    else:
        precedingweek = survey.survey_start_date - relativedelta(days=6)
        reminderdays = []
        for x in range(7):
            y = precedingweek + relativedelta(days=x)
            reminderdays.append(y)

    if request.method == "POST":
        form = BreakdownForm(users, request.POST)

        category = request.POST['category']
        reminder = request.POST['reminder']
        reminder = datetime.strptime(reminder, "%b. %d, %Y").date()

        gap = survey.survey_start_date - reminder
        gap = gap.days

        # from the form we request the otherdate from the input
        otherdate = request.POST['otherdate']
        if form.is_valid():
            obj = form.save(commit=False)
            obj.surveyentity_id = seid
            obj.surveybreakdown_category = category
            obj.surveybreakdown_reminder_date = gap
            obj.save()
            form.save_m2m()
            # dateinstances calculates all the instances that could be created from the date range
            recs = dateinstances(surveyentity.survey_start_date, surveyentity.survey_interval,
                                 surveyentity.survey_occurances)
            # to filter out the dates that are beyond our otherdate startdate we filter the dates list down
            newrecs = []
            for dategroup in recs:
                if dategroup[0][0] >= otherdate:
                    newrecs.append(dategroup)
            # we grab some other parameters from the form
            profiles = form.cleaned_data.get('profile')
            time = form.cleaned_data.get('surveybreakdown_time')
            # then we create all the instances
            for rec in newrecs:
                dd = ''.join(rec[0])
                sd = ''.join(rec[1])
                ed = ''.join(rec[2])
                for profile in profiles:
                    start = datetime.strptime(dd, "%Y-%m-%d").date()
                    rd = start - timedelta(gap)
                    SurveyInstance.objects.create(survey_date=dd, survey_time=time, surveybreakdown=obj,
                                                  survey_start_date=sd, survey_end_date=ed, profile=profile,
                                                  survey_reminder_date=rd)
            messages.success(request, 'The ' + survey.survey_name + ' survey has been updated')
            return redirect("surveybreakdownedit", sid, eid, seid)

    else:
        form = BreakdownForm(users)
    return render(request, "data/surveybreakdownadd.html",
                  {"form": form, 'breakdowncategorys': breakdowncategorys, 'reminderdays': reminderdays,
                   'survey': survey})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def surveybreakdownuseradd(request, bdid, sid, eid, seid):
    breakdown = get_object_or_404(SurveyBreakdown, pk=bdid)
    surveyentity = SurveyEntity.objects.get(pk=seid)
    survey = Survey.objects.get(pk=sid)
    allprofiles = Profile.objects.filter(entity__id=eid)
    usedprofiles = Profile.objects.filter(surveybreakdown=bdid)
    filteredprofiles = allprofiles.exclude(id__in=usedprofiles)

    if request.method == "POST":
        form = BreakdownAddUsersForm(filteredprofiles, request.POST, instance=breakdown)
        otherdate = request.POST['otherdate']
        if form.is_valid():
            profiles = form.cleaned_data.get('profile')
            for profile in profiles:
                SurveyBreakdownProfile.objects.create(surveybreakdown=breakdown, profile=profile)

            recs = dateinstances(surveyentity.survey_start_date, surveyentity.survey_interval,
                                 surveyentity.survey_occurances)
            # to filter out the dates that are beyond our otherdate startdate we filter the dates list down
            newrecs = []
            for dategroup in recs:
                if dategroup[0][0] >= otherdate:
                    newrecs.append(dategroup)
            # we grab some other parameters fromt he form
            # then we create all the instances
            for rec in newrecs:
                dd = ''.join(rec[0])
                sd = ''.join(rec[1])
                ed = ''.join(rec[2])
                for profile in profiles:
                    SurveyInstance.objects.create(survey_date=dd, survey_time=breakdown.surveybreakdown_time,
                                                  surveybreakdown=breakdown, survey_start_date=sd, survey_end_date=ed,
                                                  profile=profile)
            messages.success(request, 'The ' + survey.survey_name + ' survey has been updated')
            return redirect("surveybreakdownedit", sid, eid, seid)
    else:
        form = BreakdownAddUsersForm(filteredprofiles, instance=breakdown)
    return render(request, "data/surveybreakdownuseradd.html",
                  {'form': form, 'bdid': bdid, 'sid': sid, 'eid': eid, 'seid': seid})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def surveybreakdownuserdelete(request, pid, bdid, sid, eid, seid):
    if request.method == "POST":
        breakdownuserdelete(pid, bdid)
        messages.success(request, 'The user has been removed from this survey reminder')
        return redirect("surveybreakdownedit", sid, eid, seid)
    return render(request, "data/surveybreakdownuserdelete.html",
                  {'pid': pid, "bdid": bdid, 'sid': sid, 'eid': eid, 'seid': seid})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'centralteam'])
def surveyfinalcheck(request, sid, eid, seid):
    surveyentity = get_object_or_404(SurveyEntity, pk=seid)
    survey = get_object_or_404(Survey, pk=sid)
    entity = get_object_or_404(Entity, pk=eid)
    breakdowns = SurveyBreakdown.objects.filter(surveyentity_id=seid)
    questions = Question.objects.filter(survey_id=sid)
    profiles = Profile.objects.all()

    recs = dateinstances(surveyentity.survey_start_date, surveyentity.survey_interval, surveyentity.survey_occurances)
    reclist = []
    reclistcount = 0
    for rec in recs:
        datex = datetime.fromisoformat(rec[0][0])
        formatteddate = datex.strftime("%d %b %y")
        dd = ''.join(formatteddate)

        for breakdown in breakdowns:
            for profile in breakdown.profile.all():
                reclistcount += 1
                content = dd + " at " + str(breakdown.surveybreakdown_time.strftime(
                    "%I:%M %p")) + "<br>" + profile.first_name + " " + profile.last_name
                reclist.append([[content], [breakdown]])

    if request.method == "POST":
        SurveyEntity.objects.filter(pk=seid).update(survey_times_assigned=True)
        for rec in recs:
            dd = ''.join(rec[0])
            sd = ''.join(rec[1])
            ed = ''.join(rec[2])
            for breakdown in breakdowns:
                start = datetime.strptime(dd, "%Y-%m-%d").date()
                rd = start - timedelta(breakdown.surveybreakdown_reminder_date)
                for profile in breakdown.profile.all():
                    SurveyInstance.objects.create(survey_date=dd, survey_time=breakdown.surveybreakdown_time,
                                                  surveybreakdown=breakdown, survey_start_date=sd,
                                                  survey_reminder_date=rd, survey_end_date=ed, profile=profile)
        messages.success(request, 'The ' + survey.survey_name + ' survey has been created')
        return redirect("surveyadmin")
    return render(request, "data/surveyfinalcheck.html",
                  {"reclist": reclist, 'reclistcount': reclistcount, "survey": survey, "surveyentity": surveyentity,
                   "breakdowns": breakdowns, 'entity': entity, 'profiles': profiles, 'questions': questions})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def surveyinstance(request, sid, eid, seid):
    suveyentity = get_object_or_404(SurveyEntity, pk=seid)
    survey = get_object_or_404(Survey, pk=sid)
    entity = get_object_or_404(Entity, pk=eid)
    questions = Question.objects.filter(survey_id=sid)
    if request.method == "POST":
        form = FormSurveyEntity(request.POST, instance=suveyentity)
        if form.is_valid():
            form.save()
            return redirect("surveybreakdown", sid, eid, seid)
    else:
        form = FormSurveyEntity(instance=suveyentity)
    return render(request, "data/surveyinstance.html",
                  {"form": form, "survey": survey, "questions": questions, "entity": entity,
                   "suveyentity": suveyentity})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def surveyinstancerejection(request, siid):
    surveyinstance = get_object_or_404(SurveyInstance, pk=siid)
    if request.method == "POST":
        surveyinstance.survey_instance_complete = True
        surveyinstance.save()
        messages.success(request,
                         'The ' + surveyinstance.surveybreakdown.surveyentity.survey.survey_name
                         + ' survey has been marked as not needed')
        return redirect("mysurveys")
    return render(request, "data/surveyinstancerejection.html", {"surveyinstance": surveyinstance})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def surveyinstanceallrejection(request, siid):
    surveyinstance = get_object_or_404(SurveyInstance, pk=siid)
    if request.method == "POST":
        surveyinstance.survey_instance_complete = True
        surveyinstance.save()
        messages.success(request,
                         'The ' + surveyinstance.surveybreakdown.surveyentity.survey.survey_name
                         + ' survey has been marked as not needed')
        return redirect("allsurveys")
    return render(request, "data/surveyinstanceallrejection.html", {"surveyinstance": surveyinstance})


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['sa', 'org', 'entity', 'user', 'centralteam'])
def answers(request, siid, qid):
    # getting the associated values from the other tables related to this answer
    surveyinstance = SurveyInstance.objects.get(pk=siid)
    surveybreakdown = SurveyBreakdown.objects.get(surveyinstance=surveyinstance)
    surveyentity = SurveyEntity.objects.get(surveybreakdown=surveybreakdown)
    entity = Entity.objects.get(surveyentity=surveyentity)
    survey = Survey.objects.get(surveyentity=surveyentity)
    questions = Question.objects.filter(survey=survey)
    profile = Profile.objects.get(surveyinstance=surveyinstance)
    # the question list is used to get all the questions and to know how many questions are attached to each survey
    # it uses the answerselection function to pull in the right answer type
    questionlist = []
    for question in questions:
        answertype = answerselection(request, question.question_type, 'type')
        if answertype.objects.filter(question_id=question.id, surveyinstance_id=siid).exists():
            pass
        else:
            questionlist.append(question.id)
    # this is the question for this particular itteration
    question = Question.objects.get(pk=questionlist[qid])
    # uses the answerselection function to pull in the right answer form

    # saving the answer to the correct answer table with the question and survey instance also being saved
    if request.method == "POST":
        form = answerselection(request, question.question_type, 'form')
        if form.is_valid():
            obj = form.save(commit=False)
            obj.surveyinstance_id = siid
            obj.question_id = question.id
            obj.answer_status = True
            obj.save()
            if len(questionlist) == qid+1:  # if the number of questions left to be answer is 0...
                surveyinstance.survey_instance_complete = True
                surveyinstance.save()
                messages.success(request,
                                 'You have comepleted the '+ survey.survey_name + 'survey for ' + entity.entity_name)
                return redirect("mysurveys")  # ... then end the form ...

            return redirect("answers", siid, qid)
    else:
        form = answerselection(request, question.question_type, 'form')
    # ... otherwise go to the next question

    return render(request, "data/answers.html", {"form": form, "profile": profile, "surveybreakdown": surveybreakdown,
                                                 "surveyinstance": surveyinstance, "entity": entity, "survey": survey,
                                                 "question": question})
