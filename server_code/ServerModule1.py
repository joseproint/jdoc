import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
from anvil import *
import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime
from datetime import datetime
import bcrypt
import hashlib
import qrcode
import qrcode.image.svg
from io import BytesIO
import anvil.pdf
from anvil.pdf import PDFRenderer
#import pandas as pd
import random
import pytz
#from dateutil import parser

global df1 #pandas dataframe used in backgroundtask enviarVolante()
global cont #contador en el proceso de calcular horas
global fechaAnt
global tHoras, tHorasAnt
global empAnt
global horasAnt
global tipoAnt
global codEmpAnt
global tasaAnt
global fini
global ffin
global finiAnt
global ffinAnt
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
usuario=""

@anvil.server.callable
def userOk(email,password):
  #las lineas con # las desahabilitamos para que sea más rápido
    #user_row = app_tables.userinfo.get(userEmail=email)
    queryStr=f"""
      SELECT userName, userPass, userPassword_hash
      from userinfo
      where userEmail='{email}'
    """
    #user_row = anvil.server.call('f_extDb',queryStr,True)
    user_row = anvil.server.call('f_extDb',queryStr,True)
    if user_row is not None:
      salt = bcrypt.gensalt()
      print(f"USER_ROW:{user_row}")
      usuario=user_row['userName']
      userPass=user_row['userPass']
      stored_hash=user_row['userPassword_hash']
      #stored_hash=user_row['userPass']
      #stored_hash=user_row['userPass']
      print(f"usuario:{usuario}")
      if stored_hash is None:
        print(f"Hi {usuario}, Please reset your password with 'Forgot your password' option...")
        return None
      print(f"stored hash: {stored_hash}")
      if bcrypt.checkpw(password.encode(), stored_hash.encode()):
      #if bcrypt.checkpw(password.encode(), stored_hash):  
        #if password==stored_hash:  
        print("match")
        anvil.server.session['usuario']=usuario
        return usuario
      else:
        print("does not match")    
        blanqueaUsuario()
        return None
    else:
      print("It's not registered")
      return None

@anvil.server.callable
def hash_password2(password):
  """Hash the password using bcrypt in a way that is compatible with Python 2 and 3."""
  salt = bcrypt.gensalt()
  if not isinstance(password, bytes):
    password = password.encode()
  if not isinstance(salt, bytes):
    salt = salt.encode()

  result = bcrypt.hashpw(password, salt)

  if isinstance(result, bytes):
    return result.decode('utf-8')

@anvil.server.callable
def fPruebaHash(email,password,hashedPass):
  uRow = app_tables.userinfo.get(userEmail=email)
  uRow['userPassword_hash']=hashedPass
  uRow['userPass']=password

@anvil.server.callable
def fComparaHash(email,password):
  #print(f"email:{email} pass:{password}")
  uRow = app_tables.userinfo.get(userEmail=email)
  salt = bcrypt.gensalt()
  stored_hash = uRow['userPassword_hash']
  #print(f"storedHash:{stored_hash}")
  #isSamePassword = bcrypt.hashpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
  #if isSamePassword==True:
  #  print(f"Wellcome,password is valid")
  #else:
  #  print("Invalid password..")
  if bcrypt.checkpw(password.encode(), stored_hash.encode()):
    print("match")
  else:
    print("does not match")    

@anvil.server.callable
def fFuPago(email):
  #creo que el email no es necesario pasarlo porque el usuario ya fue validado en fUserOk
  #print(email)
  ##coachID=f_CoachRowID()
  #coachID=fCoachRowId(email)
  ##user_row=app_tables.userinfo.get_by_id(coachID)
  #user_row=app_tables.userinfo.get(userEmail=email)
  queryStr=f"""
    select userFuPago from userinfo where userEmail='{email}'
  """
  user_row = anvil.server.call('f_extDb',queryStr,True)
  #coachID=user_row.get_id()
  if user_row is not None:
    FuPago=user_row['userFuPago']
    #print(f"FuPago desde Servidor: {FuPago}")
    if FuPago is None:
      #FuPago=datetime.datetime(2020,1,1)
      FuPago=datetime(2020,1,1)
      #print(f"OK FuPago desde Servidor: {FuPago}")
  else:
    #FuPago=datetime.datetime(1950,1,1)
    FuPago=datetime(1950,1,1)
  return FuPago

@anvil.server.callable
def roleEmpleado(email):
  #user_row=app_tables.userinfo.get(userEmail=email)
  queryStr=f"""
    select userRolId from userinfo where userEmail='{email}'
  """
  user_row=anvil.server.call('f_extDb',queryStr,True)
  if user_row is not None:
    role=user_row['userRolId']
  return role

@anvil.server.callable
def blanqueaUsuario():
    anvil.server.session['usuario'] = None
    
@anvil.server.callable
def supervisor_registered(email):
  #user_row=app_tables.userinfo.get(userEmail=email)
  user_row = anvil.server.call('get_datosUsuarioSql',email)
  if user_row is not None:
    return True
  else:
    return False


@anvil.server.callable
def fEmail(origen,destino,titulo,notas):
  anvil.email.send( from_name = origen,
          from_address="support@jclock.app",         
          to=destino,
          subject = titulo,
          text= notas)
  print(f"from_name:{origen} to:{destino} subject:{titulo} texto:{notas}")
  #anvil.email.send(from_name="Rafa",from_address="support@jclock.app",to="jose@proint.com",subject="probando",text="esto es una prueba")
