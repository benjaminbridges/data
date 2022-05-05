from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('report', report, name='report'),
    path('givingreport', givingreport, name='givingreport'),
    path('allanswers', allanswers, name='allanswers'),

    #  path('downloaddata', downloaddata, name='downloaddata')

    ]