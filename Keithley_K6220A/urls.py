from django.urls import path

from Keithley_K6220A.views import *

urlpatterns = [
    path('', index, name="Keithley_K6220A")
]
