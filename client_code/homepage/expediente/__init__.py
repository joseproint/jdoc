from ._anvil_designer import expedienteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..logo import Globals
from .. import hpGlobals
import time

from datetime import datetime, timedelta
from datetime import date
global sucursal,deposito,archivo,gaveta,seccion
global rowClases, rowCbienes, server_time

class expediente(expedienteTemplate):
  def __init__(self, descripcion, expRow, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    global registrado
    global nombreAnt
    global expRowGlobal, rowClases, rowCbienes
    global sucursal,deposito,archivo,gaveta,seccion,ubiGlobal
    
    expRowGlobal=expRow
    sucursal="001"
    deposito="01"
    archivo="01"
    gaveta="01"
    seccion="01"

    if expRow is not None:
      expediente = expRow['id']
      Globals.f_setExpediente(expediente)
      
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    rowClases =  anvil.server.call('get_ClasesExpSql')
    rowCbienes = anvil.server.call('get_ClasesBienesSql')
    #cf_rows = anvil.server.call('get_CFisicas')
    ##cf_lista= [(r['cfdescripcion'],r['cfdescripcion']) for r in cf_rows]
    #cf_lista= [(r['cfdescripcion'],r) for r in cf_rows]
    #self.drop_down_cfisica.items = sorted(list(set(cf_lista)))

    #print("descripcion: "+descripcion)
    #print(sucRow['empNombre'])
    #print(sucRow['empTarifa'])
    nombreAnt = descripcion
    if descripcion is not None:
      registrado=True
      # anvil.alert("registrado")
      self.f_llenaPantalla(nombreAnt,expRow)
    else:
      registrado=False
      # anvil.alert("No registrado")
      self.llenaListas(rowClases,rowCbienes)

  def f_llenaPantalla(self, id, expRow):
    global sucursal,deposito,archivo,gaveta,seccion, ubiGlobal
    global rowClases, rowCbienes
    self.llenaListas(rowClases,rowCbienes)
    #emp_row=app_tables.clientes.get(clteNombre=nombreBuscado)
    #global cfisicaRow
    #emp_row=anvil.server.call('getClienteRow',nombreBuscado)
    #row_id = emp_row.get_id()
    ubicacion=expRow['ubicacion']
    self.text_box_codigo.text=id
    self.text_box_descripcion.text=expRow['descripcion']
    #self.txt_ubicacion.text=ubicacion
    ubiGlobal = ubicacion
    self.txt_tags.text=expRow['tags']
    clase=expRow['clase']
    cBien=expRow['claseBien']
    lat=expRow['lat']
    lng=expRow['lng']
    estBien=expRow['estadoBien']
    self.txt_etiqueta.text=expRow['etiqueta']
    self.txt_lat.text=lat
    self.txt_lng.text=lng
    #alert(f"clase: {clase}")
    #self.dd_clases.selected_value=clase
    self.dd_clases.selected_value=clase
    if cBien is not None:
      self.dd_clasesBienes.selected_value=cBien
    if estBien is not None:
      self.dd_estBien.selected_value=estBien
    
    #ubicacion='00102030405'
    sucursal =ubicacion[0:3]
    deposito =ubicacion[3:5]
    archivo =ubicacion[5:7]
    gaveta =ubicacion[7:9]
    seccion =ubicacion[9:11]

    suc = int(sucursal.lstrip("0"))
    dep = int(deposito.lstrip("0"))
    arc = int(archivo.lstrip("0"))
    gav = int(gaveta.lstrip("0"))
    sec = int(seccion.lstrip("0"))
    #suc=1
    #dep=2
    #arc=3
    #gav=4
    #sec=5
    self.dd_sucursal.selected_value = suc
    self.dd_deposito.selected_value = dep
    self.dd_archivo.selected_value = arc
    self.dd_gaveta.selected_value = gav
    self.dd_seccion.selected_value = sec
    
    #alert(f"suc:{suc} dep:{dep} arc:{arc} gav:{gav} sec:{sec}")
    #self.text_box_lat.text=emp_row['sucLat']
    #self.text_box_lng.text=emp_row['sucLng']
    #self.text_box_direccion.text=emp_row['sucDireccion']
    #self.text_box_maxradio.text=emp_row['sucMaxRadio']
    #self.drop_down_hini.selected_value=emp_row['sucHoraIni'][:2]
    #self.drop_down_mini.selected_value=emp_row['sucHoraIni'][3:]
    #self.drop_down_hout.selected_value=emp_row['sucHoraFin'][:2]
    #self.drop_down_mout.selected_value=emp_row['sucHoraFin'][3:]
    #self.marcarMapa()
    # Any code you write here will run before the form opens.

  def llenaListas(self, rowClases, rowCbienes):
    self.dd_sucursal.items = [(f"Sucursal {r}",r) for r in range(1,101)]
    self.dd_deposito.items = [(f"Deposito {r}",r) for r in range(1,11)]
    self.dd_archivo.items = [(f"Archivo {r}",r) for r in range(1,21)]
    self.dd_gaveta.items = [(f"Gaveta {r}",r) for r in range(1,9)]
    self.dd_seccion.items = [(f"Seccion {r}", r) for r in range(1,21)]
    self.dd_clases.items = [(r['descripcion'], r['id'].strip()) for r in rowClases]
    self.dd_clasesBienes.items = [(r['descripcion'], r['id'].strip()) for r in rowCbienes]
    
  def convert(self,time_string):
    date_var = time.strptime(time_string, '%H:%M')
    return date_var

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.expedientes')

  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.mainmenu')

  def actUbicacion(self):
    global sucursal,deposito,archivo,gaveta,seccion, ubiGlobal
    ubicacion=f"{sucursal}{deposito}{archivo}{gaveta}{seccion}"  
    #self.txt_ubicacion.text=ubicacion
    ubiGlobal = ubicacion
    
  def dd_sucursal_change(self, **event_args):
    """This method is called when an item is selected"""
    suc = self.dd_sucursal.selected_value
    global sucursal,deposito,archivo,gaveta,seccion
    sucursal=str(suc).zfill(3)
    self.actUbicacion()
    
  def dd_deposito_change(self, **event_args):
    """This method is called when an item is selected"""
    global sucursal,deposito,archivo,gaveta,seccion
    dep = self.dd_deposito.selected_value
    deposito=str(dep).zfill(2)
    self.actUbicacion()
    
  def dd_archivo_change(self, **event_args):
    """This method is called when an item is selected"""
    global sucursal,deposito,archivo,gaveta,seccion
    arc = self.dd_archivo.selected_value
    archivo=str(arc).zfill(2)
    self.actUbicacion()
    
  def dd_gaveta_change(self, **event_args):
    """This method is called when an item is selected"""
    global sucursal,deposito,archivo,gaveta,seccion
    gav = self.dd_gaveta.selected_value
    gaveta=str(gav).zfill(2)
    self.actUbicacion()
    
  def dd_seccion_change(self, **event_args):
    """This method is called when an item is selected"""
    global sucursal,deposito,archivo,gaveta,seccion
    sec = self.dd_seccion.selected_value
    seccion=str(sec).zfill(2)
    self.actUbicacion()

  def link_transferir_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.jdocTransfer', self)

  def link_etiqueta_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_historial_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.repeating_panel_1.items = anvil.server.call(
      'search_historial',
      self.text_box_codigo.text)

  def link_borrar_click(self, **event_args):
    """This method is called when the link is clicked"""
    save_clicked = alert(f"Are you sure you want to delete {self.text_box_descripcion.text}",
                   large=True,
                   buttons=[("yes", True), ("Cancel", False)])
    if save_clicked:
      #anvil.server.call('delete_Sucursal', self.text_box_email.text)
      anvil.server.call('deleteExpFromGridSql', self.item, self.text_box_codigo.text)
      #get_open_form().raise_event('x-refresh')
      open_form('homepage.expedientes')

  def link_salvar_click(self, **event_args):
    """This method is called when the link is clicked"""
    global nombreAnt
    global expRowGlobal
    global ubiGlobal
    global server_time
    global expediente

    server_time = anvil.server.call('ServerTimeZone')
    fecha = server_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    nombre=self.text_box_descripcion.text
    codigo=self.text_box_codigo.text
    etiqueta=self.txt_etiqueta.text
    Globals.f_setExpediente((codigo))
    
    #ubicacion=self.txt_ubicacion.text
    ubicacion = ubiGlobal
    clase = self.dd_clases.selected_value
    cBien = self.dd_clasesBienes.selected_value
    estBien = self.dd_estBien.selected_value
    
    tags=self.txt_tags.text
    codigo=codigo.strip()
    nombre=nombre.strip()
    ubicacion=ubicacion.strip()
    tags=tags.strip()
    clase=clase.strip()
    
    lat=self.txt_lat.text
    #direccion=self.text_box_direccion.text
    lng=self.txt_lng.text
    nombreNuevo = self.text_box_descripcion.text
    #maxRadio=float(self.text_box_maxradio.text)
    #hini=self.drop_down_hini.selected_value
    #hout=self.drop_down_hout.selected_value
    #mini=self.drop_down_mini.selected_value
    #mout=self.drop_down_mout.selected_value
    #horaIni=hini+":"+mini
    #horaFin=hout+":"+mout
    #anvil.alert(f"horaini:{self.convert(horaIni)} horafin:{self.convert(horaFin)}")
    
    if nombreNuevo=="" or nombreNuevo is None or nombre=="" or nombre is None:
      anvil.alert("Descripcion vacía..")
      #anvil.alert(nombre)
      #anvil.alert(nombreNuevo)
      #anvil.alert(email)
    else:
      #if nombreAnt is not None:
        #Notification("nombreAnt: "+nombreAnt)
        #registrado=anvil.server.call('f_cfRowRegistrado',nombreAnt)
        #anvil.alert(registrado)
      #  pass
      if registrado:
        #anvil.alert(f" el nombre {nombreAnt} existe y lo actualizo a {nombreNuevo}")
        # * * * ojo: <===== debo revisar como manejar esta parte * * * 
        #anvil.server.call('f_clteActualiza',SucRowGlobal, nombreAnt,nombre,email,estado,telefono,sueldo,sexo,cfisicaRow,dieta,direccion,ciudad,objetivo,diasVisita,horaVisita,horaVisita24,foto,birthday) 
        anvil.server.call('f_ExpedienteActSql',nombreAnt, nombre, ubicacion, tags, clase, etiqueta, cBien, estBien, lat, lng, codigo) 
        password="123" #temporal
        #emp_row=anvil.server.call('creaUsuarioEmp',nombre,email,password,foto)
        #emp_row=anvil.server.call('creaUsuarioEmp',nombre,email,password)
        open_form('homepage.expedientes')
        #get_open_form().raise_event('x-refresh')
      else:  
        #anvil.alert(" el nombre indicado no existe y lo creo")
        #emp_row=anvil.server.call('creaCliente',nombre,email,estado,telefono,sueldo,sexo,cfisicaRow,dieta,direccion,ciudad,objetivo,diasVisita,horaVisita,horaVisita24,foto,birthday)
        #emp_row=anvil.server.call('creaEmpleado',codigo,nombre,email,estado,telefono,sueldo,frecPago,tipoPago,sexo,direccion,ciudad,foto,birthday)
        #anvil.server.call('creaEmpleado',codigo,nombre,email,estado,telefono,sueldo,frecPago,tipoPago,sexo,direccion,ciudad,foto,birthday)
        email=Globals.f_getEmail()
        anvil.server.call('creaExpedienteSql',nombre, codigo, ubicacion, tags, clase, email, fecha, etiqueta, cBien,estBien,lat,lng)
        anvil.alert(f"Expediente {nombre} creado!")
        open_form('homepage.expedientes')

  def dd_clases_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def fDiasVencido(self,fRetorno):
    fLimite=datetime.today() + timedelta(days=-31)
    y0 = fRetorno.year
    m0 = fRetorno.month
    d0 = fRetorno.day
    #print(f"y0: {y0} m0: {m0} d0: {d0}")
    y1 = fLimite.year
    m1 = fLimite.month
    d1 = fLimite.day
    #print(f"y1: {y1} m1: {m1} d1: {d1}")
    d0 = date(y0, m0, d0)
    d1 = date(y1, m1, d1)
    dias = d1 - d0
    #print(f"Dias: {dias.days}")
    diasVencido=dias.days
    #print(f"diasfinal: {diasfinal}")
    #if diasfinal>30:
    #  return True
    #else:
    #  return False
    return diasVencido

  def link_geoloc_click(self, **event_args):
    """This method is called when the link is clicked"""
    """This method is called when the link is clicked"""
    dir = self.text_box_direccion.text
    if dir is not None:
      try:
        results = self.map_1.geocode(address=dir)
        if len(results)>0:
          latitude = results[0].geometry.location.lat()
          longitude = results[0].geometry.location.lng()   
          #position=results[0].geometry.location
          #m = Marker(position=results[0].geometry.location)
          #map.add_component(m)
          #alert(f"lat:{latitude} , lng:{longitude}")
          self.txt_lat.text=latitude
          self.txt_lng.text=longitude
          #self.marcarMapa()
      except:
          alert(f"Dirección incompleta...")