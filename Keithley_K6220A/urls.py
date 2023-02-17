from django.urls import path

from Keithley_K6220A.views import *

urlpatterns = [
    path('', index, name="Keithley_K6220A"),
    path('update_a/', update_a, name="Keithley_K6220A_update_a"),
    path('update_v/', update_v, name="Keithley_K6220A_update_v"),
    path('connect/', connect, name="Keithley_K6220A_connect"),
]
