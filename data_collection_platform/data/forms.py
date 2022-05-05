from django.forms import ModelForm, DateInput, TimeInput, NumberInput, TextInput, Textarea
from .models import *
from django.forms import modelform_factory
from colorfield.widgets import ColorWidget


class FormSurveyEntity(ModelForm):
    class Meta:
        model = SurveyEntity
        fields = '__all__'
        exclude = ['survey', 'entity', 'survey_times_assigned', 'user']
        widgets = {
            'survey_start_date': DateInput(attrs={"type": "date"}),
            'survey_time': TimeInput(attrs={"type": "time"})
        }


class SurveyAddEntitiesForm(ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['survey_name', 'category', 'survey_entity_to_set_times', 'survey_breakdown_allowed',
                   'survey_start_date', 'survey_interval', 'survey_occurances', 'survey_time', 'survey_active',
                   'survey_created_by']
        widgets = {
            'survey_description': Textarea(attrs={"type": "date"}),
            'survey_time': TimeInput(attrs={"type": "time"})
        }

    def __init__(self, filteredentities, *args, **kwargs):
        super(SurveyAddEntitiesForm, self).__init__(*args, **kwargs)
        self.fields['entity'].queryset = filteredentities


class BreakdownForm(ModelForm):
    class Meta:
        model = SurveyBreakdown
        fields = '__all__'
        exclude = ['surveyentity', 'surveybreakdown_active', 'surveybreakdown_reminder_date']
        widgets = {
            'surveybreakdown_time': TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, users,  *args, **kwargs):
        super(BreakdownForm, self).__init__(*args, **kwargs)
        self.fields['profile'].queryset = users


class BreakdownAddUsersForm(ModelForm):
    class Meta:
        model = SurveyBreakdown
        fields = '__all__'
        exclude = ['surveyentity', 'surveybreakdown_name', 'surveybreakdown_time', 'surveybreakdown_reminder_date']
        widgets = {
            'surveybreakdown_time': TimeInput(attrs={"type": "time"})
        }

    def __init__(self, filteredprofiles, *args, **kwargs):
        super(BreakdownAddUsersForm, self).__init__(*args, **kwargs)
        self.fields['profile'].queryset = filteredprofiles


class FormSurveyDatesInitial(ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['survey_name', 'category', 'entity', 'survey_entity_to_set_times', 'survey_breakdown_allowed',
                   'survey_time', 'survey_active', 'survey_created_by','survey_description']
        widgets = {
            'survey_start_date': DateInput(attrs={"type": "date"}),
        }


class FormSurveyDates(ModelForm):
    class Meta:
        model = SurveyBreakdown
        fields = '__all__'
        exclude = ['survey_name', 'category', 'entity', 'survey_entity_to_set_times', 'survey_breakdown_allowed',
                   'survey_time', 'survey_active', 'survey_created_by']


EntityForm = modelform_factory(Entity, exclude=['group'])


EntityEditForm = modelform_factory(Entity, exclude=['group', 'org'])


OrgEditForm = modelform_factory(Organisation, exclude=[])


class OrgForm(ModelForm):
    class Meta:
        model = Organisation
        fields = '__all__'
        widgets = {
            'Org color': ColorWidget
        }


class UserForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['profile_pic', 'user', 'site_permission']

    def __init__(self, entities, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['entity'].queryset = entities


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['profile_pic', 'user', 'site_permission']

    def __init__(self, entities, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['entity'].queryset = entities
        self.fields['email'].disabled = True


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'
        exclude = ['survey_interval', 'survey_occurances', 'survey_start_date',
                   'survey_time', 'survey_active', 'survey_created_by']
        widgets = {
            'survey_description': Textarea(attrs={'rows': 2}),
        }
    # this method pulls in the enties list from the view
    # then it filters the entity queryset in the form to only show those values

    def __init__(self, entities, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.fields['entity'].queryset = entities


QuestionForm = modelform_factory(Question, exclude=['survey'])


BreakdownCategoryForm = modelform_factory(BreakdownCategory, exclude=['survey'])


SurveyEntityFinalForm = modelform_factory(SurveyEntity, exclude=['survey', 'entity', 'survey_times_assigned',
                                                                 'survey_start_date', 'survey_occurances',
                                                                 'survey_interval'])


SurveyEntityForm = modelform_factory(SurveyEntity, exclude=['survey', 'entity', 'survey_times_assigned'])

# - Answer Forms - #


# class DurationAnswerForm(ModelForm):
#    class Meta:
#        model = AnswerDuration
#        fields = '__all__'
#        exclude = ['question', 'surveyinstance', 'answer_status']
#        widgets = {'answer_duration': TimeInput(attrs={"type": "time"})}


class DateAnswerForm(ModelForm):
    class Meta:
        model = AnswerDate
        exclude = ['question', 'surveyinstance', 'answer_status']
        widgets = {'answer_duration': DateInput(attrs={"type": "date"})}


class ShortTextAnswerForm(ModelForm):
    class Meta:
        model = AnswerShortText
        exclude = ['question', 'surveyinstance', 'answer_status']
        widgets = {'answer_short_text': TextInput(attrs={"autofocus": True})}


class LongTextAnswerForm(ModelForm):
    class Meta:
        model = AnswerLongText
        exclude = ['question', 'surveyinstance', 'answer_status']
        widgets = {'answer_long_text': TextInput(attrs={"autofocus": True})}


FileAnswerForm = modelform_factory(AnswerFile, exclude=['question', 'surveyinstance', 'answer_status'])


class IntegerAnswerForm(ModelForm):
    class Meta:
        model = AnswerInteger
        exclude = ['question', 'surveyinstance', 'answer_status']
        widgets = {'answer_integer': NumberInput(attrs={"autofocus": True})}


class FloatAnswerForm(ModelForm):
    class Meta:
        model = AnswerFloat
        exclude = ['question', 'surveyinstance', 'answer_status']
        widgets = {'answer_float': NumberInput(attrs={"autofocus": True})}


MoneyAnswerForm = modelform_factory(AnswerCurrency, exclude=['question', 'surveyinstance', 'answer_status'])
