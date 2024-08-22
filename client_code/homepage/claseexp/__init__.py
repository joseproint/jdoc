from ._anvil_designer import clasexpTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time

class claseexp(claseexpTemplate):
  def __init__(self, descripcion, sucRow, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    global registrado
    global nombreAnt
    global SucRowGlobal

    SucRowGlobal=sucRow
    
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

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
      self.f_llenaPantalla(nombreAnt,sucRow)
    else:
      registrado=False
      # anvil.alert("No registrado")

  def f_llenaPantalla(self, nombreBuscado, sucRow):
    #emp_row=app_tables.clientes.get(clteNombre=nombreBuscado)
    #global cfisicaRow
    #emp_row=anvil.server.call('getClienteRow',nombreBuscado)
    emp_row=sucRow
    #row_id = emp_row.get_id()
    self.text_box_nombre.text=nombreBuscado
    self.text_box_lat.text=emp_row['sucLat']
    self.text_box_lng.text=emp_row['sucLng']
    self.text_box_direccion.text=emp_row['sucDireccion']
    self.text_box_maxradio.text=emp_row['sucMaxRadio']
    self.drop_down_hini.selected_value=emp_row['sucHoraIni'][:2]
    self.drop_down_mini.selected_value=emp_row['sucHoraIni'][3:]
    self.drop_down_hout.selected_value=emp_row['sucHoraFin'][:2]
    self.drop_down_mout.selected_value=emp_row['sucHoraFin'][3:]
    self.marcarMapa()
    # Any code you write here will run before the form opens.

  def button_salvar_click(self, **event_args):
    """This method is called when the button is clicked"""
    global nombreAnt
    global SucRowGlobal

    nombre=self.text_box_nombre.text
    lat=self.text_box_lat.text
    direccion=self.text_box_direccion.text
    lng=self.text_box_lng.text
    nombreNuevo = self.text_box_nombre.text
    maxRadio=float(self.text_box_maxradio.text)
    hini=self.drop_down_hini.selected_value
    hout=self.drop_down_hout.selected_value
    mini=self.drop_down_mini.selected_value
    mout=self.drop_down_mout.selected_value
    horaIni=hini+":"+mini
    horaFin=hout+":"+mout
    #anvil.alert(f"horaini:{self.convert(horaIni)} horafin:{self.convert(horaFin)}")
    
    if nombreNuevo=="" or nombreNuevo is None or nombre=="" or nombre is None or direccion=="" or direccion is None:
      anvil.alert("Name can not be blank")
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
        anvil.server.call('f_sucActualiza',SucRowGlobal, nombreAnt,nombre,lat,lng,direccion,maxRadio,horaIni,horaFin) 
        password="123" #temporal
        #emp_row=anvil.server.call('creaUsuarioEmp',nombre,email,password,foto)
        #emp_row=anvil.server.call('creaUsuarioEmp',nombre,email,password)
        open_form('homepage.sucursales')
        #get_open_form().raise_event('x-refresh')
      else:  
        #anvil.alert(" el nombre indicado no existe y lo creo")
        #emp_row=anvil.server.call('creaCliente',nombre,email,estado,telefono,sueldo,sexo,cfisicaRow,dieta,direccion,ciudad,objetivo,diasVisita,horaVisita,horaVisita24,foto,birthday)
        #emp_row=anvil.server.call('creaEmpleado',codigo,nombre,email,estado,telefono,sueldo,frecPago,tipoPago,sexo,direccion,ciudad,foto,birthday)
        #anvil.server.call('creaEmpleado',codigo,nombre,email,estado,telefono,sueldo,frecPago,tipoPago,sexo,direccion,ciudad,foto,birthday)
        anvil.server.call('creaSucursal',nombre,lat,lng,direccion,maxRadio,horaIni,horaFin)
        anvil.alert(f"Branch {nombre} created!")
        open_form('homepage.sucursales')

  def convert(self,time_string):
    date_var = time.strptime(time_string, '%H:%M')
    return date_var

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    save_clicked = alert(f"Are you sure you want to delete {self.text_box_nombre.text}",
                   large=True,
                   buttons=[("yes", True), ("Cancel", False)])
    if save_clicked:
      #anvil.server.call('delete_Sucursal', self.text_box_email.text)
      anvil.server.call('deleteSucFromGridSql', self.item, self.text_box_nombre.text)
      #get_open_form().raise_event('x-refresh')
      open_form('homepage.sucursales')

  def button_cancel_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('homepage.sucursales')

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.sucursales')

  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage')

  def link_geoloc_click(self, **event_args):
    """This method is called when the link is clicked"""
    dir = self.text_box_direccion.text
    try:
      results = self.map_1.geocode(address=dir)
      if len(results)>0:
        latitude = results[0].geometry.location.lat()
        longitude = results[0].geometry.location.lng()   
        #position=results[0].geometry.location
        #m = Marker(position=results[0].geometry.location)
        #map.add_component(m)
        #alert(f"lat:{latitude} , lng:{longitude}")
        self.text_box_lat.text=latitude
        self.text_box_lng.text=longitude
        self.marcarMapa()
    except:
        alert(f"Dirección incompleta...")
      
  def marcarMapa(self):
    latitude=self.text_box_lat.text
    longitude=self.text_box_lng.text
    if latitude!=0 and longitude!=0:
      marker = self.map_1.Marker(
        animation=self.map_1.Animation.DROP,
        position=self.map_1.LatLng(latitude,longitude)
        )
      self.map_1.add_component(marker)
      self.map_1.center = marker.position
      self.map_1.zoom = 13

