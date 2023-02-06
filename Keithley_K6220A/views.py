from django.http import HttpResponse
from django.shortcuts import render, redirect

device = { 'name':'Keithley_K6220A',
            'status': 'disconnected',
            'value': '--- --',
            'amper_value': '0',
            'volt_value': '0',
        }

def is_connect():
    return True

# Должен сразу проверять подключение и узнавать текущее значение
def index(request):
    if is_connect:
        device['status'] = 'connected'
        device['value'] = '55 mA' # узнавать текущее значение
    else:
        device['status'] = 'disconnected'
        device['value'] = '--- --'
    return render(request, 'Keithley_K6220A/index.html', {'device': device})


# Должен подключать и узнавать текущее значение
def connect(request):
    if request.method == 'POST':
        device['status'] = 'connected' # Must be connecting
        device['value'] = '55 mA' # узнавать текущее значение
        device['amper_value'] = '0' # clear
        device['volt_value'] = '0' # clear
        context = {
            'device': device, 
        }
        return redirect('/' + str(device['name']) + '/', context=context)


def disconnect(request):
    if request.method == 'POST':
        device['status'] = 'disconnected' # Must be connecting
        device['value'] = '--- --' # узнавать текущее значение
        device['amper_value'] = '0' # clear
        device['volt_value'] = '0' # clear
        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)
    

def update_a(request):
     if request.method == 'POST':
        device['value'] = '17.2mA'
        device['amper_value'] = request.POST['ampers']
        context = {
            'device': device, 
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)
     
def update_v(request):
     if request.method == 'POST':
        device['value'] = '1.2mA'
        device['volt_value'] = request.POST['volts']
        context = {
            'device': device, 
            'volts': 0,
        }
        return redirect(request.META.get('HTTP_REFERER', '/'), context=context)