from django.http import HttpResponse
from django.shortcuts import render, redirect
from time import sleep
from .Yokogawa_GS200 import *
from app.utils import formatValue

yoko = None

def index(request):
    global yoko
    if yoko is None:
        try:
            # print("Moment 0")
            # rm = visa.ResourceManager()
            # print("Moment 1")
            # rm.open_resource('USB0::0x0B21::0x0039::91VB13481::0::INSTR')
            # print("Moment 2")
            yoko = Yokogawa_GS210('USB0::0x0B21::0x0039::91VB13481::INSTR')
            print("Moment 3")

        except Exception as e:
            yoko = None

    if yoko and yoko.is_enabled():
        device = { 'name': 'Yokogawa_GS210',
            'name_replace': 'Yokogawa GS210',
            'status': 'connected',
            'current_on': yoko.get_status(),
            'value': formatValue(yoko.get_current()),
            'amper_value': formatValue(yoko.get_current())[:-2],
            'volt_value': yoko.get_voltage_compliance(),
            'unit_a': formatValue(yoko.get_current())[-2:],
            'unit_v': 'V',
        }
    else:
        yoko = None

        # Здесь по плану yoko обнулился после выключения
        device = { 'name': 'Yokogawa_GS210',
                'name_replace': 'Yokogawa GS210',
                'status': 'disconnected',
                'current_on': 0,
                'value': '--- --',
                'amper_value': '0',
                'volt_value': '0',
                'unit_a': 'mA',
                'unit_v': 'V',
            }


    return render(request, 'Yokogawa_GS210/index.html', {'device': device})


# Должен подключать и узнавать текущее значение
def connect(request):
    if request.method == 'POST':
        global yoko
        if yoko and yoko.is_enabled():
            if yoko.get_status():
                yoko.set_status(0)
            else:
                yoko.set_status(1)

        return redirect('/Yokogawa_GS210/')
            


def update_a(request):
     if request.method == 'POST':
        global yoko
        if yoko and yoko.is_enabled():
            units = {
                "mA":"e-3",
                "uA":"e-6",
            }
            ampers = float(request.POST['ampers'] + units[request.POST['ampers_type']])
            yoko.set_current(ampers)

        return redirect(request.META.get('HTTP_REFERER', '/'))
     
def update_v(request):
     if request.method == 'POST':
        global yoko
        if yoko and yoko.is_enabled():
            volts = 0 if request.POST['volts'] == '' else float(request.POST['volts'])
            yoko.set_voltage_compliance(volts)

        return redirect(request.META.get('HTTP_REFERER', '/'))