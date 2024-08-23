from ._anvil_designer import expedienteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
global sucursal,deposito,archivo,gaveta,seccion
global rowClases

class expediente(expedienteTemplate):
  def __init__(self, descripcion, clasRow, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    global registrado
    global nombreAnt
    global ClasRowGlobal, rowClases
    global sucursal,deposito,archivo,gaveta,seccion
    
    ClasRowGlobal=clasRow
    sucursal="001"
    deposito="01"
    archivo="01"
    gaveta="01"
    seccion="01"
    
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    rowClases =  anvil.server.call('get_ClasesExpSql')
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
      self.f_llenaPantalla(nombreAnt,clasRow)
    else:
      registrado=False
      # anvil.alert("No registrado")

  def f_llenaPantalla(self, id, clasRow):
    global sucursal,deposito,archivo,gaveta,seccion
    global rowClases
    #emp_row=app_tables.clientes.get(clteNombre=nombreBuscado)
    #global cfisicaRow
    #emp_row=anvil.server.call('getClienteRow',nombreBuscado)
    #row_id = emp_row.get_id()
    ubicacion=clasRow['ubicacion']
    self.text_box_codigo.text=id
    self.text_box_descripcion.text=clasRow['descripcion']
    self.txt_ubicacion.text=ubicacion
    self.txt_tags.text=clasRow['tags']
    clase=clasRow['clase']
    self.dd_clases.selected_value=clase
    
    #ubicacion='00102030405'
    sucursal =ubicacion[0:3]
    deposito =ubicacion[3:5]
    archivo =ubicacion[5:7]
    gaveta =ubicacion[7:9]
    seccion =ubicacion[9:11]
    
    #alert(f"suc:{sucursal} dep:{deposito} arc:{archivo} gav:{gaveta} sec:{seccion}")
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

    self.dd_sucursal.items = [(f"Sucursal {r}",r) for r in range(100)]
    self.dd_deposito.items = [(f"Deposito {r}",r) for r in range(10)]
    self.dd_archivo.items = [(f"Archivo {r}",r) for r in range(20)]
    self.dd_gaveta.items = [(f"Gaveta {r}",r) for r in range(8)]
    self.dd_seccion.items = [(f"Seccion {r}", r) for r in range(20)]
    self.dd_clases.items = [(r['descripcion'], r) for r in rowClases]
    
  def button_salvar_click(self, **event_args):
    """This method is called when the button is clicked"""
    global nombreAnt
    global ClasRowGlobal

    nombre=self.text_box_descripcion.text
    codigo=self.text_box_codigo.text
    ubicacion=self.txt_ubicacion.text
    clase = self.txt_clase.text
    tags=self.txt_tags.text
    codigo=codigo.strip()
    nombre=nombre.strip()
    ubicacion=ubicacion.strip()
    tags=tags.strip()
    
    #lat=self.text_box_lat.text
    #direccion=self.text_box_direccion.text
    #lng=self.text_box_lng.text
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
        anvil.server.call('f_ExpedienteActSql',nombreAnt, nombre, ubicacion, tags, clase, codigo) 
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
        anvil.server.call('creaExpedienteSql',nombre, codigo, ubicacion, tags, clase)
        anvil.alert(f"Branch {nombre} created!")
        open_form('homepage.expedientes')

  def convert(self,time_string):
    date_var = time.strptime(time_string, '%H:%M')
    return date_var

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    save_clicked = alert(f"Are you sure you want to delete {self.text_box_descripcion.text}",
                   large=True,
                   buttons=[("yes", True), ("Cancel", False)])
    if save_clicked:
      #anvil.server.call('delete_Sucursal', self.text_box_email.text)
      anvil.server.call('deleteExpFromGridSql', self.item, self.text_box_codigo.text)
      #get_open_form().raise_event('x-refresh')
      open_form('homepage.expedientes')

  def btn_etiqueta_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('homepage.expedientes')

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.expedientes')

  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.mainmenu')

  def actUbicacion(self):
    global sucursal,deposito,archivo,gaveta,seccion
    ubicacion=f"{sucursal}{deposito}{archivo}{gaveta}{seccion}"  
    self.txt_ubicacion.text=ubicacion
    
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
    