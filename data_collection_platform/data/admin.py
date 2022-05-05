from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(Organisation)
admin.site.register(Group)
admin.site.register(Entity)

admin.site.register(Survey)
admin.site.register(EntityGroup)
admin.site.register(SurveyEntity)

admin.site.register(SurveyBreakdown)
admin.site.register(SurveyBreakdownProfile)
admin.site.register(BreakdownCategory)

admin.site.register(SurveyInstance)
admin.site.register(Question)
# admin.site.register(Category)

# admin.site.register(AnswerDuration)

admin.site.register(AnswerDate)
admin.site.register(AnswerFloat)
admin.site.register(AnswerCurrency)
admin.site.register(AnswerInteger)
admin.site.register(AnswerFile)
admin.site.register(AnswerLongText)
admin.site.register(AnswerShortText)

