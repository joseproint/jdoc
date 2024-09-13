import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.pdf
from anvil.pdf import PDFRenderer
import io
import base64
import anvil.media
import anvil.http
import urllib.request
import time


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
import pyodbc
import pymssql
from decimal import Decimal
import json
import datetime
#from datetime import datetime

def connectMysql():
  connection = pymysql.connect(host='127.0.0.1',
                               port=3306,
                               user='root',
                               #password=anvil.secrets.get_secret('db_password'),
                               password='r4m2007',
                               database='jclock',
                               cursorclass=pymysql.cursors.DictCursor)

  return connection

def connectODBCSQLServer():
  #Coneccion a Microsoft SQLServer usando pyodbc module from Microsoft
  #SERVER = 'sntswjpspn01.jostens.com'
  #DATABASE = 'jClock'
  #USERNAME = 'svc_sntapps'
  #PASSWORD = 'oBHa#45*vjQP65'
  
  SERVER = 'LENOVO'
  DATABASE = 'jDoc'
  USERNAME = 'sa'
  PASSWORD = 'r4m2007'
  
  connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
  connection = pyodbc.connect(connectionString)
  
  return connection

def connect():
  #Coneccion a Microsoft SQLServer usando pymssql module from community
  connection = pymssql.connect(
      #server='sntswjpspn01.jostens.com',
      #port=1433,
      #user='svc_sntapps',
      #password='oBHa#45*vjQP65',
      #database='jClock',
      
      server='LENOVO',
      port=1433,
      user='sa',
      password='r4m2007',
      database='jDoc',
      as_dict=True
  )
  
  return connection

@anvil.server.callable
def f_extData(queryStr):
  #print(queryStr)
  conn=connect()
  cur=conn.cursor(as_dict=True)
  cur.execute(queryStr)
  rowAf=cur.fetchall()
  cur.close()
  conn.close()
  #print(rowAf)
  as_json = json.dumps(rowAf, default=json_dumps_default, sort_keys=False, indent=2) #para evitar error serializacion numeros y fechas de sqlserver
  as_json = json.loads(as_json) 
  print(f"as_json {as_json}")
  return as_json
  
@anvil.server.callable
def f_extDb(queryStr,oneRecord):
  print(queryStr)
  conn=connect()
  #cur=conn.cursor()
  cur=conn.cursor(as_dict=True)
  cur.execute(queryStr)
  if oneRecord is True:
    rowAf=cur.fetchone()
  else:
    rowAf=cur.fetchall()
  cur.close()
  conn.close()
  #print(rowAf)
  #userName=rowAf['userName']
  #print(f"username before change: {userName}")
  as_json = json.dumps(rowAf, default=json_dumps_default, sort_keys=False, indent=2) #para evitar error serializacion numeros y fechas de sqlserver
  as_json = json.loads(as_json) 
  #print(f"json loaded: {as_json}")
  return as_json

def json_dumps_default(obj):
    # ref: http://stackoverflow.com/a/16957370/2144390
    # evita el error de serializacion de los campos tipos numeros y fechas de sqlserver
    #if isinstance(obj, datetime.datetime):
    #    return str(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return str(obj)   
    if isinstance(obj, datetime.date):
        return str(obj)
    raise TypeError

@anvil.server.callable
def SQLServerTest():
  queryStr=f"""
    SELECT * FROM SUCURSALES
  """
  registros = f_extDb(queryStr,False)
  print(f"registros pymssql: {registros}")
  as_json = json.dumps(registros, default=json_dumps_default, sort_keys=False, indent=2)
  print(f"registros json: {as_json}")
  return as_json
  
@anvil.server.callable
def get_datosSucursal(sucursal):
  queryStr=f"""
    SELECT * from sucursales where sucNombre='{sucursal}'
  """
  rowSuc = f_extDb(queryStr,True)
  return rowSuc
  
@anvil.server.callable
def get_totalPonches(email):
  #queryStr=f"""
  #  SELECT COUNT(ponCodEmp) as cantidad from ponches where ponEmailEmp='{email}'
  #"""
  respuesta=""
  #print(queryStr)
  try:
    conn=connect()
    #cur=conn.cursor()
    cur=conn.cursor(as_dict=True)
    #cur.execute(queryStr)
    cur.callproc('getTotalPonches',(email,))
    #print(f"param1:{params[0]}")
    #print(f"param2:{params[1]}")
    rowAf=cur.fetchall()
    #rowAf=cur
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
  finally:
    if conn:
      cur.close()
      conn.close()
      for row in rowAf:
        print(row['cantidad'])
  #print(rowAf)
  #print(f"rowaf[0]:{rowAf[0]}")
  #print(f"rowaf[1]:{rowAf[1]}")
  #rowAf = json.dumps(rowAf, default=json_dumps_default, sort_keys=False, indent=2) #para evitar error serializacion numeros y fechas de sqlserver
  #rowAf = json.loads(rowAf) 

  if rowAf is not None:
    #cantidad=rowAf['cantidad']
    cantidad=rowAf[0]['cantidad']
  else:
    cantidad=0
  print("la cantidad es: {cantidad}")  
  return cantidad

@anvil.server.callable
def get_firstPonche(email):
  #queryStrMySql=f"""
  #  SELECT ponTipo from ponches where ponEmailEmp='{email}'
  #  order by ponFechaHora Desc
  #  LIMIT 1
  #"""
  #Sql Server:
  #queryStr=f"""
  #  SELECT TOP 1 ponTipo from ponches where ponEmailEmp='{email}'
  #  order by ponFechaHora Desc
  #"""
  #print(queryStr)
  #rowAf = f_extDb(queryStr,True)
  try:
    conn=connect()
    cur=conn.cursor(as_dict=True)
    cur.callproc('getFirstPunch',(email,))
    rowAf=cur.fetchall()
    #cur.execute(queryStr)
    #rowAf=cur.fetchone()
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
  finally:
    if conn:
      cur.close()
      conn.close()
  #print(rowAf)
  return rowAf

@anvil.server.callable
def get_lastPonche(email):
  #queryStrMySql=f"""
  #  SELECT ponFechaHora from ponches where ponEmailEmp='{email}'
  #  order by ponFechaHora desc
  #  LIMIT 1
  #"""
  #queryStrSqlServer=f"""
  #  SELECT TOP 1 ponFechaHora from ponches where ponEmailEmp='{email}'
  #  order by ponFechaHora desc
  #"""
  #print(queryStrSqlServer)
  #rowAf = f_extDb(queryStrSqlServer,True)
  try:
    conn=connect()
    cur=conn.cursor(as_dict=True)
    cur.callproc('getLastPunch',(email,))
    rowAf=cur.fetchall()
  
    #cur.execute(queryStr)
    #rowAf=cur.fetchone()
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
  finally:
    if conn:
      cur.close()
      conn.close()
  #print(rowAf)
  return rowAf

@anvil.server.callable
def get_datosEmp(email):
  #queryStr=f"""
  #  SELECT empCoachID, empTasaHora, empEmail, empCodigo, empCiudad, empDireccion, empTelefono, empSueldo, empTipoPago, empFrecPago, empStatus, empSexo, empBirthday
  #  from empleados where empEmail='{email}'
  #"""
  #print(queryStr)
  #rowAf = f_extDb(queryStr,True)
  
  start_time = time.time()
  try:
    conn=connect()
    cur=conn.cursor(as_dict=True)
    cur.callproc('getDatosEmp',(email,))
    rowAf=cur.fetchall()
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
  finally:
    if conn:
        cur.close()
        conn.close()
  end_time = time.time()
  execution_time = start_time - end_time
  print(f"get_DatosEmp execution time of {email}:{execution_time}")

  ##cur.execute(queryStr)
  ##rowAf=cur.fetchone()
  #cur.close()
  #conn.close()
  ###print(rowAf)
  return rowAf

@anvil.server.callable
def InsertaPonche(codEmp,emailEmp,fechaDT,horaStr,fechaStr,lat,lng,tPonche,ciaEmail,tPoncheAnt,diff_in_hours, tasaHora,tSucursal):
  date_format = '%Y/%m/%d %H:%M:%S'  
  #fechaDT=datetime.datetime.strftime(fechaDT,date_format)  
    
  data=(codEmp,emailEmp,fechaDT,horaStr,fechaStr,lat,lng,tPonche,ciaEmail,tPoncheAnt,diff_in_hours,tasaHora,tSucursal)
  queryStr=f"""
    INSERT INTO PONCHES (ponCodEmp,ponEmailEmp,ponFechaHora,ponHora,ponFecha,ponLat,ponLng,ponTipo,ponCiaEmail,ponFechaHoraAnt,ponHoras, ponTasaHora,ponSucursal)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
  """
  comandoSql(queryStr,data)
  ActualizaPonche(fechaDT,tPonche,emailEmp)
  
def ActualizaPonche(fechaDT,tPonche,emailEmp):
  data=(fechaDT,tPonche,emailEmp)
  queryStr=f"""
    UPDATE empleados SET ponFechaHora=%s, ponTipo=%s 
     WHERE empEmail=%s
  """
  comandoSql(queryStr,data)    

@anvil.server.callable
def InsertaEmpSql(codigo,nombre, email, estado, telefono, sueldo, frecPago, tasaHora, tipoPago,sexo, direccion, ciudad, foto, coachID, birthday):
  data=(codigo,nombre, email, estado, telefono, sueldo, frecPago, tasaHora, tipoPago,sexo, direccion, ciudad, coachID, birthday)
  queryStr = f"""
    INSERT INTO EMPLEADOS (empCodigo,empNombre, empEmail, empStatus, empTelefono, empSueldo, empFrecPago, empTasaHora, empTipoPago,empSexo, empDireccion, empCiudad, empCoachID,empBirthday )
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
  """
  #data=json.load(data)
  print(f"data:{data}")
  comandoSql(queryStr,data)
  
@anvil.server.callable
def InsertaUserSql(username,email,password,pwhash,role,userlinkey):
  data=(username,email,password,pwhash,role,userlinkey)
  queryStr = f"""
    INSERT INTO USERINFO (userName,userEmail, userPass, userPassword_hash, userRolId, userLink_key)
    VALUES(%s, %s, %s, %s, %s, %s)
  """
  #data=json.load(data)
  comandoSql(queryStr,data)

@anvil.server.callable
def creaSucursalSql(nombre, lat, lng, direccion, maxRadio, horaIni,horaFi):
  data = (nombre, lat, lng, direccion, maxRadio, horaIni,horaFi)
  queryStr = f"""
    INSERT INTO SUCURSALES (sucNombre, sucLat, sucLng, sucDireccion, sucMaxRadio, sucHoraIni,sucHoraFin)
    VALUES(%s, %s, %s, %s, %s, %s, %s)
  """
  print(f"queryStr {queryStr} data {data}")
  comandoSql(queryStr,data)

@anvil.server.callable
def creaClaseExpSql(nombre, id):
  data = (id, nombre)
  queryStr = f"""
    INSERT INTO CLASESEXP (id, descripcion)
    VALUES(%s, %s)
  """
  print(f"queryStr {queryStr} data {data}")
  comandoSql(queryStr,data)

@anvil.server.callable
def creaClaseBienSql(nombre, id):
  data = (id, nombre)
  queryStr = f"""
    INSERT INTO CLASESBIENES (id, descripcion)
    VALUES(%s, %s)
  """
  print(f"queryStr {queryStr} data {data}")
  comandoSql(queryStr,data)
  
@anvil.server.callable
def creaExpedienteSql(nombre, id, ubicacion, tags, clase, email, fcreacion, etiqueta, cBien,estBien,lat,lng):
  data = (id, nombre, ubicacion, tags, clase, email, fcreacion, etiqueta, cBien,estBien,lat,lng)
  queryStr = f"""
    INSERT INTO EXPEDIENTES (id, descripcion, ubicacion, tags, clase, creadopor, fcreacion, etiqueta, claseBien,estadoBien,lat,lng)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
  """
  print(f"queryStr {queryStr} data {data}")
  comandoSql(queryStr,data)
  
@anvil.server.callable
def get_perfilUsuario(email):
  queryStr=f"""
      SELECT empNombre, empEmail, empCoachID from empleados where
      empEmail='{email}'
  """
  rowUsuario = f_extDb(queryStr,True)
  return rowUsuario

@anvil.server.callable
def get_datosUsuario(nombre):
  queryStr=f"""
    SELECT userName, userEmail, userCiaName, userPhone, userLunchTime from userInfo where userName='{nombre}'
  """
  print(queryStr)
  rowAf = f_extDb(queryStr,True)
  #conn=connect()
  #cur=conn.cursor()
  #cur.execute(queryStr)
  #rowAf=cur.fetchone()
  #cur.close()
  #conn.close()
  print(rowAf)
  return rowAf

@anvil.server.callable
def get_datosUsuarioSql(email):
  queryStr=f"""
    SELECT userName, userEmail, userCiaName, userPass, userConfirmed_email, userPassword_hash, userLink_key from userInfo where userEmail='{email}'
  """
  print(queryStr)
  rowAf = f_extDb(queryStr,True)
  #conn=connect()
  #cur=conn.cursor()
  #cur.execute(queryStr)
  #rowAf=cur.fetchone()
  #cur.close()
  #conn.close()
  print(rowAf)
  return rowAf

@anvil.server.callable
def fguardaUserLinkSql(email, usertoken):
  #user_row['userLink_key'] = usertoken
  data=(usertoken,email)
  queryStr=f"""
    UPDATE USERINFO SET userLink_key=%s 
     WHERE userEmail=%s
  """
  print(f"queryStr {queryStr} data:{data}")
  #  #actualizo el ponche de salida
  comandoSql(queryStr,data)  
  
@anvil.server.callable
def get_foto(id):
  conn = connect()
  with conn.cursor() as cur:
    queryStr=f"""
     select userImage
     from userinfo
     where userName = '{id}'
    """
    cur.execute(queryStr)
    rowAf=cur.fetchone()
    cur.close()
    conn.close()
    newfoto=None
    if rowAf is not None:
      print('aqui voy get_foto()...')
      foto=rowAf['userImage']
      if foto is not None:
        newfoto=anvil.BlobMedia("image/png",foto)
    return newfoto

@anvil.server.callable
def get_ponchesXRango(fini,ffin,email):
  queryStr=f"""
    SELECT * from ponches where
      ponEmailEmp='{email}'
      and ponFechaHora >= '{fini}'
      and ponFechaHora <= '{ffin}'
      and ponTipo = 'O'
      order by ponEmailEmp Asc
  """
  rowPonches = f_extDb(queryStr,False)
  return rowPonches

@anvil.server.callable
def get_ponchesSql(fini,ffin,email,coachID):
  queryStr=f"""
    SELECT * from ponches where
      ponEmailEmp='{email}'
      and ponFechaHoraAnt >= '{fini}'
      and ponFechaHoraAnt <= '{ffin}'
      and ponTipo = 'O'
      and ponCiaEmail= '{coachID}'
      order by ponFechaHora Asc
  """
  rowPonches = f_extDb(queryStr,False)
  return rowPonches

@anvil.server.callable
def get_ponchesxRangoCia(fini,ffin,coachID):
  queryStr=f"""
    SELECT * from ponches where
      ponFechaHora >= '{fini}'
      and ponFechaHora <= '{ffin}'
      and ponCiaEmail = '{coachID}'
      order by ponEmailEmp, ponFechaHora Asc
  """
  rowPonches = f_extDb(queryStr,False)
  return rowPonches

@anvil.server.callable
def get_ponchesxCia(fini,ffin,coachID):
  #  SELECT ponCodEmp,ponEmailEmp,ponFecha,ponHora,ponTipo,ponCiaEmail from ponches where
  queryStr=f"""
    SELECT ponCodEmp,ponEmailEmp,ponFechaHora,ponTipo,ponCiaEmail from ponches where
      ponFechaHora >= '{fini}'
      and ponFechaHora <= '{ffin}'
      and ponCiaEmail = '{coachID}'
      order by ponEmailEmp, ponFechaHora Asc
  """
  rowPonches = f_extDb(queryStr,False)
  return rowPonches

@anvil.server.callable
def get_empleadosSql(status,coachID):
  if status=='T': #todos los empleados
    queryStr=f"""
      SELECT empCodigo,empNombre,empCoachID, empTelefono, empStatus, empEmail, empDireccion,empCiudad,empSexo,empFrecPago,empTipoPago,empBirthday,empSueldo
      from empleados
      order by empNombre Asc
    """
  else: #solo los empleados con el status indicado
    queryStr=f"""
      SELECT empCodigo,empNombre,empCoachID, empTelefono, empStatus 
      from empleados where
        empStatus='{status}'
        order by empNombre Asc
    """
  print(queryStr)
  rowEmp = f_extDb(queryStr,False)
  return rowEmp
  
@anvil.server.callable
def get_EmpleadoSql(nombre):
  queryStr=f"""
      SELECT empCodigo,empNombre,empCoachID, empEmail
      from empleados where
        empNombre = '{nombre}'
  """
  rowEmp = f_extDb(queryStr,True)
  return rowEmp

@anvil.server.callable
def get_SucursalesSql():
  queryStr=f"""
      SELECT * from sucursales
  """
  rowSucursales = f_extDb(queryStr,False)
  return rowSucursales

@anvil.server.callable
def get_ClasesExpSql():
  queryStr=f"""
      SELECT * from clasesExp
  """
  rowCExp = f_extDb(queryStr,False)
  return rowCExp

@anvil.server.callable
def get_ClasesBienesSql():
  queryStr=f"""
      SELECT * from clasesBienes
  """
  rowCBien = f_extDb(queryStr,False)
  return rowCBien
  
@anvil.server.callable
def get_ExpedientesSql():
  queryStr=f"""
      SELECT * from Expedientes
  """
  rowExp = f_extDb(queryStr,False)
  return rowExp

@anvil.server.callable
def get_expSearchSql(dato):
  queryStr=f"""
      SELECT * from Expedientes
      where id like '%{dato}%'
      or descripcion like '%{dato}%'
      or tags like '%{dato}%'
      or clase like '%{dato}%'
      or etiqueta like '%{dato}%'
  """
  rowExp = f_extDb(queryStr,False)
  return rowExp

@anvil.server.callable
def get_expSearchDeepSql(whereStr):
  queryStr=f"""
      SELECT * from Expedientes
  """
  queryStr = f"{queryStr} {whereStr}"
  print(queryStr)
  rowExp = f_extDb(queryStr,False)
  return rowExp
  
@anvil.server.callable
def get_expHistorySql(dato):
  queryStr=f"""
      SELECT * from exptrack
      where codexpediente ='{dato}'
      order by ftransaccion desc
  """
  rowHist = f_extDb(queryStr,False)
  return rowHist
  
@anvil.server.callable
def actualizaPoncheSQL(row,fechaOriginal,poncheIni,poncheFin,email,empresa,fechaEntrada):
    if row is not None:
      date_format = '%m/%d/%Y %H:%M:%S'  
      poncheIni=datetime.datetime.strptime(poncheIni,date_format)  
      poncheFin=datetime.datetime.strptime(poncheFin,date_format)  
      diff = poncheFin - poncheIni
      # Get interval between two timstamps in hours
      diff_in_hours = diff.total_seconds() / 3600
      #row['ponHoras']=diff_in_hours
      #row['ponFechaHoraAnt']=poncheIni
      #row['ponFechaHora']=poncheFin
      
      #para actualizar el ponche de salida
      queryStr=f"""
        UPDATE PONCHES SET ponHoras=%s, ponFechaHoraAnt=%s, ponFechaHora=%s 
        WHERE ponEmailEmp=%s and ponFechaHora=%s and ponSucursal=%s
      """
      data = (diff_in_hours,poncheIni,poncheFin,email,fechaOriginal,empresa)
      
      #para actualizar el ponche de entrada
      queryStr2=f"""
        UPDATE PONCHES SET ponFechaHora=%s 
        WHERE ponEmailEmp=%s and ponFechaHora=%s and ponSucursal=%s and ponTipo='I'
      """
      data2 = (poncheIni,email,fechaEntrada,empresa)
      
      queryTest=f"""
        UPDATE PONCHES SET ponFechaHora='{poncheIni}' 
        WHERE ponEmailEmp='{email}' and ponFechaHora='{fechaEntrada}' and ponSucursal='{empresa}' and ponTipo='I'
      """
      print(f"quesryTest {queryTest}")
      #  #actualizo el ponche de salida
      comandoSql(queryStr,data)

      #actualizo el ponche de entrada
      comandoSql(queryStr2,data2)

@anvil.server.callable
def deleteFromGridSQL(row,fechaOriginal,email,empresa,fechaEntrada):
    if row is not None:
      #borra la salida
      queryStr=f"""
        DELETE FROM PONCHES 
        WHERE ponEmailEmp=%s and ponFechaHora=%s and ponSucursal=%s
      """
      data = (email,fechaOriginal,empresa)
      print(f"{queryStr} Data:{data}")
      comandoSql(queryStr,data)

      #borra la entrada
      queryStr2=f"""
        DELETE FROM PONCHES 
        WHERE ponEmailEmp=%s and ponFechaHora=%s and ponSucursal=%s
      """
      data2 = (email,fechaEntrada,empresa)
      print(f"{queryStr2} Data:{data2}")
      comandoSql(queryStr2,data2) 

@anvil.server.callable
def deleteEmpFromGridSql(row,codEmp,empresa):
    if row is not None:
      #borra la salida
      queryStr=f"""
        DELETE FROM EMPLEADOS 
        WHERE empCodigo=%s
      """
      data = (codEmp)
      print(f"{queryStr} Data:{data}")
      comandoSql(queryStr,data)

@anvil.server.callable
def deleteSucFromGridSql(row,nombreSuc):
    if row is not None:
      queryStr=f"""
        DELETE FROM SUCURSALES 
        WHERE sucNombre='{nombreSuc}'
      """
      #data = (nombreSuc)
      print(f"{queryStr}")
      deleteSql(queryStr)

@anvil.server.callable
def deleteCExpFromGridSql(row,nombreExp):
    if row is not None:
      queryStr=f"""
        DELETE FROM CLASESEXP 
        WHERE sucNombre='{nombreExp}'
      """
      #data = (nombreSuc)
      print(f"{queryStr}")
      deleteSql(queryStr)

@anvil.server.callable
def deleteCBienFromGridSql(row,nombreExp):
    if row is not None:
      queryStr=f"""
        DELETE FROM CLASESBIENES 
        WHERE descripcion='{nombreExp}'
      """
      #data = (nombreSuc)
      print(f"{queryStr}")
      deleteSql(queryStr)
      
@anvil.server.callable
def deleteExpFromGridSql(row,id):
    if row is not None:
      queryStr=f"""
        DELETE FROM EXPEDIENTES 
        WHERE id='{id}'
      """
      #data = (nombreSuc)
      print(f"{queryStr}")
      deleteSql(queryStr)
         
@anvil.server.callable
def delete_EmpleadoSql(email,empresa):
    queryStr=f"""
      DELETE FROM EMPLEADOS 
      WHERE empEmail='{email}'
    """
    #data = (email)
    print(f"{queryStr}")
    deleteSql(queryStr)

@anvil.server.callable
def delete_userSql(email,empresa):
    queryStr=f"""
      DELETE FROM USERINFO 
      WHERE userEmail='{email}'
    """
    #data = (email)
    print(f"{queryStr}")
    deleteSql(queryStr)
      
@anvil.server.callable
def comandoSql(queryStr,data):
    try:
      conn=connect()
      cur=conn.cursor()
      as_json = json.dumps(data, default=json_dumps_default, sort_keys=False, indent=2) #para evitar error serializacion numeros y fechas de sqlserver
      dataok = json.loads(as_json) 
      print(f"tuple de dataok:{tuple(dataok)}")
      cur.execute(queryStr, tuple(dataok))
      conn.commit()
      print(tuple(dataok))
    #except pymysql.MySQLError as e:
    except pymssql.Error as e:
      print('Got error {!r}, errno is {}'.format(e, e.args[0]))
      conn.rollback()
    cur.close()
    conn.close()

@anvil.server.callable
def deleteSql(queryStr):
    try:
      conn=connect()
      cur=conn.cursor()
      #as_json = json.dumps(data, default=json_dumps_default, sort_keys=False, indent=2) #para evitar error serializacion numeros y fechas de sqlserver
      #dataok = json.loads(as_json) 
      #cur.execute(queryStr, tuple(dataok))
      cur.execute(queryStr)
      conn.commit()
      #print(tuple(dataok))
    except pymssql.Error as e:
      print('Got error {!r}, errno is {}'.format(e, e.args[0]))
      conn.rollback()
    cur.close()
    conn.close()

@anvil.server.callable
def f_empActualizaSql(empRow, nombreViejo,cNombre,cEmail,cEstado,cTelefono,cSueldo,cFrecPago,cTipoPago,cSexo,cDireccion,cCiudad,foto,birthday,cCodigo):
    if cNombre is not None:
      if cTipoPago=='Hour':
        cFrecPago = 'Hourly'

      from . import Nomina
      tasaHora = Nomina.f_tasaHora(cSueldo,cFrecPago)
      
      queryStr=f"""
      UPDATE EMPLEADOS SET empCodigo=%s,empNombre=%s,empEmail=%s,empStatus=%s,empTelefono=%s,empSueldo=%s,empFrecPago=%s,empTipoPago=%s,
        empSexo=%s,empBirthday=%s,empDireccion=%s,empCiudad=%s,empTasaHora=%s
        WHERE empEmail=%s
      """
      data=(cCodigo,cNombre,cEmail,cEstado,cTelefono,cSueldo,cFrecPago,cTipoPago,cSexo,birthday,cDireccion,cCiudad,tasaHora,cEmail)
      print(f"queryStr {queryStr} datos {data}")
      comandoSql(queryStr,data)
    else:
      Notification('New name is empty')

@anvil.server.callable
def f_sucActualizaSql(nombreAnt,nombre,lat,lng,direccion,maxRadio,horaIni,horaFin):
  if nombre is not None:
      queryStr=f"""
      UPDATE SUCURSALES SET sucNombre=%s,sucLat=%s,sucLng=%s,sucDireccion=%s,sucMaxRadio=%s,sucHoraIni=%s,sucHoraFin=%s
        WHERE sucNombre=%s
      """
      data=(nombre,lat,lng,direccion,maxRadio,horaIni,horaFin,nombreAnt)
      print(f"queryStr {queryStr} datos {data}")
      comandoSql(queryStr,data)
  else:
    Notification('New name is empty')

@anvil.server.callable
def f_claseExpActualizaSql(nombreAnt,nombre, id):
  if nombre is not None:
      queryStr=f"""
      UPDATE CLASESEXP SET descripcion=%s
        WHERE id=%s
      """
      data=(nombre,id)
      print(f"queryStr {queryStr} datos {data}")
      comandoSql(queryStr,data)
  else:
    Notification('Nueva descripción está vacía..')

@anvil.server.callable
def f_claseBienActualizaSql(nombreAnt,nombre, id):
  if nombre is not None:
      queryStr=f"""
      UPDATE CLASESBIENES SET descripcion=%s
        WHERE id=%s
      """
      data=(nombre,id)
      print(f"queryStr {queryStr} datos {data}")
      comandoSql(queryStr,data)
  else:
    Notification('Nueva descripción está vacía..')

@anvil.server.callable
def f_ExpedienteActSql(nombreAnt,nombre, ubicacion, tags, clase, etiqueta, cBien, estBien, lat, lng, id):
  if nombre is not None:
      queryStr=f"""
      UPDATE EXPEDIENTES SET descripcion=%s, ubicacion=%s, tags=%s, clase=%s, etiqueta=%s, claseBien=%s, estadoBien=%s, lat=%s, lng=%s
        WHERE id=%s
      """
      data=(nombre,ubicacion,tags,clase,etiqueta,cBien,estBien,lat,lng,id)
      print(f"queryStr {queryStr} datos {data}")
      comandoSql(queryStr,data)
  else:
    Notification('Nueva descripción está vacía..')
    
@anvil.server.callable
def f_userActualizaSql(nombre,email,telefono,ciaName,lunchTime,nombreAnt):
  if nombre is not None:
      queryStr=f"""
      UPDATE USERINFO SET userEmail=%s,userPhone=%s,userCiaName=%s,userLunchTime=%s
          WHERE userName=%s
      """
      data=(email,telefono,ciaName,lunchTime,nombreAnt)
      print(f"queryStr {queryStr} datos {data}")
      comandoSql(queryStr,data)
  else:
    Notification('Datos Usuario en blanco')

@anvil.server.callable
def f_userUpdateSql(passHash,userPass,userLink,email):
  if email is not None:
      #queryStr=f"""
      #UPDATE USERINFO SET userPassword_hash=%s,userPass=%s,userLink_key=%s
      #    WHERE userEmail=%s
      #"""
      queryStr=f"""
      UPDATE USERINFO SET userPassword_hash=%s,userLink_key=%s
          WHERE userEmail=%s
      """
      data=(passHash,userLink,email)
      print(f"queryStr {queryStr} datos {data}")
      comandoSql(queryStr,data)
  else:
    Notification('Invalid User Info...')

@anvil.server.callable
def f_userConfirmEmailSql(confirmedEmail,userLink,email):
  if email is not None:
      queryStr=f"""
      UPDATE USERINFO SET userConfirmed_email=%s,userLink_key=%s
          WHERE userEmail=%s
      """
      data=(confirmedEmail,userLink,email)
      print(f"queryStr {queryStr} datos {data}")
      comandoSql(queryStr,data)
  else:
    Notification('Invalid ser Info...')

@anvil.server.callable
def get_datosUsuarioSql(email):
  queryStr=f"""
    SELECT userName, userEmail, userCiaName, userPass, userConfirmed_email, userPassword_hash, userLink_key from userInfo where userEmail='{email}'
  """
  print(queryStr)
  rowAf = f_extDb(queryStr,True)
  #conn=connect()
  #cur=conn.cursor()
  #cur.execute(queryStr)
  #rowAf=cur.fetchone()
  #cur.close()
  #conn.close()
  print(rowAf)
  return rowAf

@anvil.server.callable
def createSend_pdf(pantalla,fecha,etiqueta,codigoaf,codemp,cia,loc,depto,lat,lng,firma,notas,descripcion):
  pdfReport=None
  if pantalla=='Transferencia EXP':
     pdfReport = PDFRenderer(filename=f'TransferenciaEXP.pdf').render_form('homepage.jdocTransfer_copy',fecha,etiqueta,codigoaf,codemp,cia,loc,depto,lat,lng,firma,notas,descripcion)
  return pdfReport

@anvil.server.callable
def transfiereExp(fecha,codExpediente,empRecibe,empEntrega,notas,tipotrans,numTransf,fRetorno):
  #tipotrans='TRANSFERENCIA'
  transferenciaOk=True
  queryStr=f"""
    SELECT MAX(numtrans) as ultimo from EXPTRACK 
    WHERE tipotrans='{tipotrans}'
  """
  rowUltimo = f_extDb(queryStr,True)
  if rowUltimo is not None:
    ultimo=rowUltimo['ultimo']
    if ultimo is not None:
      numtrans = ultimo + 1
    else:
      numtrans = 1
  else:
    numtrans = 1
  data= (tipotrans,numtrans,fecha,codExpediente,empRecibe,empEntrega,notas,fRetorno)
  queryStr=f"""
     INSERT INTO EXPTRACK (tipotrans,numtrans,ftransaccion,codexpediente,empRecibe,empEntrega,notas,fRetorno) 
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
    """
  print(queryStr)
  comandoSql(queryStr,data)
  if tipotrans=='ACUSERECIBO':
    numRecibo=numtrans
    data = (numRecibo,numTransf)
    queryStr=f"""
      UPDATE EXPTRACK SET NUMRECIBO=%s 
      WHERE TIPOTRANS='TRANSFERENCIA' AND NUMTRANS=%s;
      """
    print(queryStr)
    comandoSql(queryStr,data)
  return transferenciaOk

@anvil.server.callable
def f_nombreEmpleado(email):
  nombre=None
  queryStr=f"""
  SELECT empNombre as nombre from empleados
    WHERE empEmail='{email}'
  """
  rowEmp = f_extDb(queryStr,True)
  if rowEmp is not None:
    nombre=rowEmp['nombre']
  else:
    nombre=None
  return nombre

@anvil.server.callable
def f_contactoEmpleado(email):
  nombre=None
  queryStr=f"""
  SELECT empNombre as nombre, empTelefono as telefono from empleados
    WHERE empEmail='{email}'
  """
  rowEmp = f_extDb(queryStr,True)
  if rowEmp is not None:
    nombre=rowEmp['nombre']
    telefono=rowEmp['telefono']
    dato=(f"{nombre} ({telefono[:3]}) {telefono[3:6]}-{telefono[6:]}")
  else:
    nombre=None
    telefono=None
    dato=None
  return dato
  
@anvil.server.callable
def get_estadosBien():
  rowEstado = ['Disponible','Rentado','Vendido','Todos']
  return rowEstado


@anvil.server.callable
def get_ExpedientesAll(clase,estado):
  conn = connect()
  with conn.cursor() as cur:
    #queryStr=f"""
    # select id, descripcion, lat, lng, claseBien, estadoBien
    # from EXPEDIENTES
    # where claseBien = '{clase}'
    # and estadoBien = '{estado}'
    #"""
    #  queryStr=f"""
    #  select id, descripcion, lat, lng, claseBien, estadoBien
    #  from EXPEDIENTES
    #  where claseBien = '{clase}'
    #  """
    queryStr=f"""
    select id, descripcion, lat, lng, claseBien, estadoBien
    from EXPEDIENTES
    """
    if clase=='zTodos':
      if estado=='Todos':
        whereStr=""
      else:
        whereStr=f" where estadoBien = '{estado}'"
    else:
      if estado=='Todos':
        whereStr=f" where claseBien = '{clase}'"
      else:
        whereStr=f" where claseBien = '{clase}' and estadoBien = '{estado}'"
    queryStr=f"{queryStr} {whereStr}"    
    print(f"queryStr:{queryStr}")
    cur.execute(queryStr)
    rowAf =  cur.fetchall()
    #rowAf=cur.fetchone()
    cur.close()
    conn.close()
    #print(rowAf)
    lista=datosAFAjson(rowAf)
    return lista

def datosAFAjson(dataRow):
  cont=1
  jsonData=''
  for r in dataRow:
    if cont>1:
      dato=', {"id": "'+f"{r['id']}"+'", "descripcion": "'+f"{r['descripcion']}"+'", "lat": "'+f"{r['lat']}"+'", "lng": "'+f"{r['lng']}"+'", "claseBien": "'+f"{r['claseBien']}"+'", "estadoBien": "'+f"{r['estadoBien']}"+'"'+'}'
    else:  
      dato='{"id": "'+f"{r['id']}"+'", "descripcion": "'+f"{r['descripcion']}"+'", "lat": "'+f"{r['lat']}"+'", "lng": "'+f"{r['lng']}"+'", "claseBien": "'+f"{r['claseBien']}"+'", "estadoBien": "'+f"{r['estadoBien']}"+'"'+'}'
    jsonData = jsonData + dato 
    cont=cont+1
  jsonData='['+jsonData+']'
  return jsonData
