from django.http import HttpResponse
from django.shortcuts import render, redirect
from time import sleep
from .Yokogawa_GS200 import *
from app.utils import formatValue

class CurrentSource:
    def __init__(self):
        self.yoko = 0
        self.connect_device()


    def connect_device(self):
        try:
            print('yoko 2')
            if self.yoko:
                print('yoko 3')
                # Пытаюсь закрыть, если успешно то пытаюсь создать новый
                # self.yoko.clear()
                print("AFTer clear")
                # self.yoko.close()
                print("After close")
                if self.yoko.get_id() != 'YOKOGAWA,GS211,91VB13481,2.02\n':
                    self.yoko = 0
                # self.yoko = Yokogawa_GS210('USB0::0x0B21::0x0039::91VB13481::INSTR')
                # else:
                #     print('yoko 4')
                #     return 0
            else:
                print('yoko 5')
                self.yoko = Yokogawa_GS210('USB0::0x0B21::0x0039::91VB13481::INSTR')

        except Exception as e:
            print('yoko 6')
            print(e)
            self.yoko = 0


cs = CurrentSource()
# # Возвращает либо подключенный девайс либо 0 если он отключен
# def connect_device():
#     try:
#         print('yoko BEFORE')
#         # yoko = Yokogawa_GS210('USB0::0x0B21::0x0039::91VB13481::INSTR')
#         print('yoko 2')
#         if yoko:
#             print('yoko 3')
#             # Пытаюсь закрыть, если успешно то пытаюсь создать новый
#             # if True:
#             yoko.clear()
#             print("AFTer clear")
#             yoko.close()
#             print("After close")
#             # yoko.get_id() == 'YOKOGAWA,GS211,91VB13481,2.02\n'
#             yoko = Yokogawa_GS210('USB0::0x0B21::0x0039::91VB13481::INSTR')
#             return yoko
#             # else:
#             #     print('yoko 4')
#             #     return 0
#         else:
#             print('yoko 5')
#             yoko = Yokogawa_GS210('USB0::0x0B21::0x0039::91VB13481::INSTR')
#             return yoko

    # except Exception as e:
    #     print('yoko 6')
    #     print(e)
    #     return 0

# Должен сразу проверять подключение и узнавать текущее значение
def index(request):
    cs.connect_device()
    if cs.yoko:
        device = { 'name': 'Yokogawa_GS210',
                'name_replace': 'Yokogawa GS210',
                'status': 'connected',
                'current_on': cs.yoko.get_status(),
                'value': formatValue(cs.yoko.get_current()),
                'amper_value': formatValue(cs.yoko.get_current())[:-2],
                'volt_value': cs.yoko.get_voltage_compliance(),
                'unit_a': formatValue(cs.yoko.get_current())[-2:],
                'unit_v': 'V',
            }
    else:
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
        cs.connect_device()
        if cs.yoko:
            if cs.yoko.get_status():
                cs.yoko.set_status(0)
            else:
                cs.yoko.set_status(1)

        return redirect('/Yokogawa_GS210/')
            


def update_a(request):
     if request.method == 'POST':
        cs.connect_device()
        if cs.yoko:
            units = {
                "mA":"e-3",
                "uA":"e-6",
            }
            ampers = float(request.POST['ampers'] + units[request.POST['ampers_type']])
            cs.yoko.set_current(ampers)

        return redirect(request.META.get('HTTP_REFERER', '/'))
     
def update_v(request):
     if request.method == 'POST':
        cs.connect_device()
        if cs.yoko:
            volts = 0 if request.POST['volts'] == '' else float(request.POST['volts'])
            cs.yoko.set_voltage_compliance(volts)

        return redirect(request.META.get('HTTP_REFERER', '/'))