import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .homepage.logo import Module1
#
#    Module1.say_hello()
#
global lastform
global username
global email
global password
global label1
global label2
global label3
global fini
global ffin
global dictHoras
global tablaStr
global empresa
global empEmail

def say_hello():
  print("Hello, world")

def f_setLastform(form):
  global lastform
  lastform = form

def f_getLastform():
  global lastform
  return lastform

def f_setSignupForm(uName,uEmail,uPass):
  global username
  global email
  global password
  username = uName
  email = uEmail
  password = uPass

def f_setEmailEmp(eEmail):
  global empEmail
  empEmail = eEmail
  
def f_setEmail(uEmail):
  global email
  email = uEmail

def f_setUsername(uName):
  global username
  username = uName
  
def f_getUsername():
  global username
  return username

def f_getEmail():
  global email
  return email

def f_getEmailEmp():
  global empEmail
  return empEmail
  
def f_getPassword():
  global password
  return password

def f_inicializa():
  global username
  global email
  global password
  global empresa
  empresa = ""
  username=""
  email=""
  password=""
  tablaStr=""

def f_getEmpresa():
  global empresa
  return empresa

def f_getLabel1():
  global label1
  return label1

def f_getLabel2():
  global label2
  return label2

def f_getLabel3():
  global label3
  return label3

def f_getFini():
  global fini
  return fini
  
def f_getFfin():
  global ffin
  return ffin

def f_setFini(ini):
  global fini
  fini = ini

def f_setFfin(fin):
  global ffin
  ffin = fin

def f_setLabel1(label):
  global label1
  label1 = label

def f_setLabel2(label):
  global label2
  label2 = label

def f_setLabel3(label):
  global label3
  label3 = label

def f_setEmpresa(cia):
  global empresa
  empresa = cia
  
def f_getDictHoras():
  global dictHoras
  return dictHoras

def f_setDictHoras(dictH):
  global dictHoras
  dictHoras=dictH

def f_getTablaStr():
  global tablaStr
  return tablaStr

def f_setTablaStr(tabla):
  global tablaStr
  tablaStr=tabla
