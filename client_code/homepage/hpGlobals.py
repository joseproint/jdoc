import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import datetime
import time
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .homepage import Module1
#
#    Module1.say_hello()
#
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .homepage import Module1
#
#    Module1.say_hello()
#

global abierto
global formSelf
global longitud
global latitud
  
def f_getLng():
  global longitud
  return longitud

def f_getLat():
  global latitud
  return latitud

def f_setLng(lng):
  global longitud
  longitud = lng

def f_setLat(lat):
  global latitud
  latitud = lat
  
def f_setFormSelf(fSelf):
  global formSelf
  formSelf = fSelf

def f_getFormSelf():
  global formSelf
  return formSelf

def f_setAbierto(status):
  #True or False
  global abierto
  abierto=status
  
def f_getAbierto():
  global abierto
  return abierto

def f_inicializa():
  global abierto
  global formSelf
  abierto=False
  formSelf=[]

def f_fechaHoy():
    now = time.localtime()
    #weekday_index = now.tm_wday
    #nombreDia=WEEKDAYS[weekday_index]
    fecha=datetime.datetime
    #nombreMes=anvil.server.call('f_nombreMes',fecha.now().month)
    #fechaHoy=f"{nombreDia} {nombreMes} {fecha.now().day}th {fecha.now().year}"
    fechaHoy=datetime.datetime(fecha.now().year,fecha.now().month,fecha.now().day)
    #print(fechaHoy)
    return fechaHoy

def f_fechaHoraHoy():
    fecha=datetime.datetime.now()
    return fecha

def f_fecha():
    now = time.localtime()
    #weekday_index = now.tm_wday
    #nombreDia=WEEKDAYS[weekday_index]
    fecha=datetime.datetime
    #nombreMes=anvil.server.call('f_nombreMes',fecha.now().month)
    #fechaHoy=f"{nombreDia} {nombreMes} {fecha.now().day}th {fecha.now().year}"
    fechaHoy=datetime.date(fecha.now().year,fecha.now().month,fecha.now().day)
    #print(fechaHoy)
    return fechaHoy

def f_fechaStrToDT(date_str):
  #date_str = '2023-02-28 14:30:00'
  date_format = '%Y-%m-%d %H:%M:%S'
  date_obj = datetime.strptime(date_str, date_format)
  print(date_obj)
  return date_obj
  