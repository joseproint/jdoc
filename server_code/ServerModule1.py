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
  #coachID=f_CoachRowID()
  coachID=f_CoachRowId(email)
  #user_row=app_tables.userinfo.get_by_id(coachID)
  user_row=app_tables.userinfo.get(userEmail=email)
  coachID=user_row.get_id()
  if user_row is not None:
    FuPago=user_row['userFuPago']
    #print(f"FuPago desde Servidor: {FuPago}")
    if FuPago is None:
      FuPago=datetime.datetime(2020,1,1)
      #print(f"OK FuPago desde Servidor: {FuPago}")
  else:
    FuPago=datetime.datetime(1950,1,1)
  return FuPago

@anvil.server.callable
def f_CoachRowID():
  usuario = anvil.server.session.get('usuario')
  #cRow = app_tables.userinfo.get(userName=usuario)
  cRow = anvil.server.call('get_datosUsuario',usuario)
  if cRow is not None:
    email = cRow['userEmail']
    #rowID = app_tables.userinfo.get(userEmail=email).get_id()
    #return rowID
    return email
  else:
    return None

@anvil.server.callable
def roleEmpleado(email):
  user_row=app_tables.userinfo.get(userEmail=email)
  if user_row is not None:
    role=user_row['userRolId']
  return role

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
def get_Empleados(status):
  coachID=f_CoachRowID()
  ##print(f"CoachID: {coachID}")
  ##print(f"Estatus: {status}")
  ##if status=='T':
  ##  return app_tables.empleados.search(tables.order_by("empCodigo",ascending=True), empCoachID=coachID)
  ##else:  
  ##  return app_tables.empleados.search(empStatus=status,empCoachID=coachID)
  rowEmpleados=anvil.server.call('get_empleadosSql',status,coachID)  
  return rowEmpleados

@anvil.server.callable
def search_Empleados(query,status):
  coachID=f_CoachRowID()
  if status=='T':
    #trae todos los empleados del coach indicado
    #result = app_tables.empleados.search(empCoachID=coachID)
    result = anvil.server.call('get_empleadosSql',status,coachID)
  else:  
    #result = app_tables.empleados.search(empStatus=status,empCoachID=coachID)
    result = anvil.server.call('get_empleadosSql',status,coachID)
  if query:
    result = [
      x for x in result
      if query in x['empNombre']
      #or query in x['last_name']
      #or query in str(x['pay_grade'])
      #or query in x['team']
    ]
  return result

@anvil.server.callable
def creaEmpleado(codigo,nombre,email,estado,telefono,sueldo,frecPago,tipoPago,sexo,direccion,ciudad,foto,birthday):
  if tipoPago=='Hour':
    frecPago='Hourly'
  from . import Nomina
  tasaHora = Nomina.f_tasaHora(sueldo,frecPago)
  coachID = f_CoachRowID()
  #if not empRegistrado(email):
    # creo el cliente porque no está registrado
    #emp_row = app_tables.clientes.add_row(clteNombre=nombre, clteEmail=email, clteStatus=estado, clteTelefono=telefono, clteTarifa=precio, clteSexo=sexo, clteCFisica=cfisicaRow, clteDieta=dieta, clteDireccion=direccion, clteCiudad=ciudad, clteObjetivo=objetivo, clteDiasVisita=diasvisita, clteHoraVisita=horavisita, clteHoraVisita24=horavisita24, clteFoto=foto, clteCoachID=fUserRowId(),clteBirthday=birthday )
  #emp_row = app_tables.empleados.add_row(empCodigo=codigo,empNombre=nombre, empEmail=email, empStatus=estado, empTelefono=telefono, empSueldo=sueldo, empFrecPago=frecPago, empTasaHora=tasaHora, empTipoPago=tipoPago,empSexo=sexo, empDireccion=direccion, empCiudad=ciudad, empFoto=foto, empCoachID=f_CoachRowID(),empBirthday=birthday )
  anvil.server.call('InsertaEmpSql',codigo,nombre, email, estado, telefono, sueldo, frecPago, tasaHora, tipoPago,sexo, direccion, ciudad, foto, coachID, birthday)
  # print(f"Customer {emp_row['clteNombre']} created")
    #return emp_row
  #else:
    # actualizo los datos del cliente
  #  emp_row=app_tables.clientes.get(clteEmail=email)
  #  emp_row['empCodigo']=codigo
  #  emp_row['empNombre']=nombre
  #  emp_row['empEmail']=email
  #  emp_row['empTelefono']=telefono
  #  emp_row['empSueldo']=sueldo
  #  emp_row['empSexo']=sexo
  #  emp_row['empDireccion']=direccion
  #  emp_row['empCiudad']=ciudad
  #  emp_row['empFoto']=foto
  #  emp_row['empBirthday']=birthday
  #  # print(f"Customer {emp_row['empNombre']} updated!")
  #  #return emp_row

@anvil.server.callable
def creaUsuarioEmp(username,email,password,foto):
    pwhash = hash_password(password, bcrypt.gensalt())
    role="Empleado" #para no presentar pantalla bloqueo por falta de pago
    #user_row=app_tables.userinfo.add_row(userName=username,userEmail=email, userPass=password, userImage=foto, userPassword_hash=pwhash, userRolId=role)
    userlinkey = None
    anvil.server.call('InsertaUserSql',username,email,password,pwhash,role, userlinkey)
    #user_row['userLink_key']=None
    #return user_row

@anvil.server.callable
def search_Expediente(query):
  coachID=f_CoachRowID()
  if status=='T':
    #trae todos los empleados del coach indicado
    #result = app_tables.empleados.search(empCoachID=coachID)
    result = anvil.server.call('get_empleadosSql',status,coachID)
  else:  
    #result = app_tables.empleados.search(empStatus=status,empCoachID=coachID)
    result = anvil.server.call('get_empleadosSql',status,coachID)
  if query:
    result = [
      x for x in result
      if query in x['empNombre']
      #or query in x['last_name']
      #or query in str(x['pay_grade'])
      #or query in x['team']
    ]
  return result