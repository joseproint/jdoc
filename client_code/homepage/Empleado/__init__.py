from ._anvil_designer import EmpleadoTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..logo import Globals

nombreAnt = ""
registrado = False
EmpRowGlobal = None

class Empleado(EmpleadoTemplate):
  def __init__(self, descripcion, EmpRow, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    global registrado
    global nombreAnt
    global EmpRowGlobal

    EmpRowGlobal=EmpRow
    
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

    #cf_rows = anvil.server.call('get_CFisicas')
    ##cf_lista= [(r['cfdescripcion'],r['cfdescripcion']) for r in cf_rows]
    #cf_lista= [(r['cfdescripcion'],r) for r in cf_rows]
    #self.drop_down_cfisica.items = sorted(list(set(cf_lista)))

    #print("descripcion: "+descripcion)
    #print(EmpRow['empNombre'])
    #print(EmpRow['empTarifa'])
    nombreAnt = descripcion
    if descripcion is not None:
      registrado=True
      # anvil.alert("registrado")
      #email = Globals.f_getEmailEmp()
      #empresa = Globals.f_getEmpresa()
      #email = EmpRow['empEmail']
      #EmpRow = anvil.server.call('get_datosEmp',email)
      #EmpRowGlobal=EmpRow
      self.f_llenaPantalla(nombreAnt,EmpRow)
    else:
      registrado=False
      # anvil.alert("No registrado")

  def f_llenaPantalla(self, nombreBuscado, EmpRow):
    #emp_row=app_tables.clientes.get(clteNombre=nombreBuscado)
    #global cfisicaRow
    #emp_row=anvil.server.call('getClienteRow',nombreBuscado)
    print(f"EmpRow:{EmpRow}")
    emp_row=EmpRow
    #row_id = emp_row.get_id()
    self.text_box_nombre.text=nombreBuscado
    self.text_box_email.text=emp_row['empEmail']
    self.text_box_codigo.text=emp_row['empCodigo']
    #self.text_area_goal.text=emp_row['empObjetivo']
    self.text_box_ciudad.text=emp_row['empCiudad']
    self.text_box_direccion.text=emp_row['empDireccion']
    self.text_box_sueldo.text=emp_row['empSueldo']
    tipoPago=emp_row['empTipoPago']
    frecPago=emp_row['empFrecPago']
    if tipoPago is None:
      tipoPago="Hour"
    if frecPago is None:
      frecPago="Weekly"
    self.drop_down_paytype.selected_value=tipoPago
    self.drop_down_payfrec.selected_value=frecPago
    self.text_box_telefono.text=emp_row['empTelefono']
    #cfisicaRow=emp_row['empCFisica']
    #cfdescripcion=cfisica['cfdescripcion']
    #self.drop_down_cfisica.selected_value=cfisicaRow
    #cf_row=anvil.server.call('getCfRow',cfisica)
    #self.drop_down_cfisica.selected_value[cfdescripcion]
    cStatus=emp_row['empStatus']
    if cStatus=='A':
      self.radio_button_activo.selected=True
    elif cStatus=='I':
      self.radio_button_inactivo.selected=True
    elif cStatus=='H':
      self.radio_button_hold.selected=True
    cSexo=emp_row['empSexo']
    if cSexo=='M':
      self.radio_button_masculino.selected=True
      self.radio_button_femenino.selected=False
    elif cSexo=='F':
      self.radio_button_femenino.selected=True
      self.radio_button_masculino.selected=False
    #cDieta=emp_row['empDieta']
    #if cDieta=='S':
    #  self.radio_button_sidieta.selected=True
    #  self.radio_button_nodieta.selected=False
    #elif cDieta=='N':
    #  self.radio_button_nodieta.selected=True
    #  self.radio_button_sidieta.selected=False
    #diasVisita=emp_row['empDiasVisita']
    #fDesglosaDias(self, diasVisita)
    #horaVisita=emp_row['empHoraVisita']
    #horaVisita24 = anvil.server.call('f_horaF24',horaVisita)
    ##print("Hora F12: "+horaVisita)
    ##print("Hora F24: "+horaVisita24)
    #self.drop_down_hora.selected_value=horaVisita
    #self.image_foto.source=emp_row['empFoto']
    self.date_picker_birthday.date=emp_row['empBirthday']

  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage')

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.Empleados')

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    save_clicked = alert(f"Are you sure you want to delete {self.text_box_nombre.text}",
                   large=True,
                   buttons=[("yes", True), ("Cancel", False)])
    if save_clicked:
      #anvil.server.call('delete_Empleado', self.text_box_email.text)
      empresa = Globals.f_getEmpresa()
      anvil.server.call('delete_EmpleadoSql', self.text_box_email.text, empresa)
      anvil.server.call('delete_userSql',self.text_box_email.text,empresa)
      #get_open_form().raise_event('x-refresh')
      open_form('homepage.Empleados')

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file != None:
      self.image_foto.source=file
    else:
      anvil.alert('FileLoader is not working')

  def button_salvar_click(self, **event_args):
    """This method is called when the button is clicked"""
    global nombreAnt
    #global cfisicaRow
    global EmpRowGlobal

    codigo=self.text_box_codigo.text
    nombre=self.text_box_nombre.text
    email=self.text_box_email.text
    estado=self.radio_button_activo.get_group_value()
    telefono=self.text_box_telefono.text
    sueldo=float(self.text_box_sueldo.text)
    frecPago=self.drop_down_payfrec.selected_value
    tipoPago=self.drop_down_paytype.selected_value
    sexo=self.radio_button_masculino.get_group_value()
    #cfisicaRow=self.drop_down_cfisica.selected_value
    birthday=self.date_picker_birthday.date
    #dieta=self.radio_button_sidieta.get_group_value()
    direccion=self.text_box_direccion.text
    ciudad=self.text_box_ciudad.text
    #objetivo=self.text_area_goal.text
    nombreNuevo = self.text_box_nombre.text
    #diasVisita = fDiasVisita(self)
    #horaVisita = self.drop_down_hora.selected_value
    #horaVisita24 = anvil.server.call('f_horaF24',horaVisita)
    foto = self.image_foto.source
    if nombreNuevo=="" or nombreNuevo is None or nombre=="" or nombre is None or email == "" or email is None or sueldo is None:
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
        ##anvil.alert(f" el nombre {nombreAnt} existe y lo actualizo a {nombreNuevo}")
        ## * * * ojo: <===== debo revisar como manejar esta parte * * * 
        ##anvil.server.call('f_clteActualiza',EmpRowGlobal, nombreAnt,nombre,email,estado,telefono,sueldo,sexo,cfisicaRow,dieta,direccion,ciudad,objetivo,diasVisita,horaVisita,horaVisita24,foto,birthday) 
        #anvil.server.call('f_empActualiza',EmpRowGlobal, nombreAnt,nombre,email,estado,telefono,sueldo,frecPago,tipoPago,sexo,direccion,ciudad,foto,birthday,codigo) 
        anvil.server.call('f_empActualizaSql',EmpRowGlobal, nombreAnt,nombre,email,estado,telefono,sueldo,frecPago,tipoPago,sexo,direccion,ciudad,foto,birthday,codigo)         
        password="123" #temporal
        ##emp_row=anvil.server.call('creaUsuarioEmp',nombre,email,password,foto)
        #anvil.server.call('creaUsuarioEmp',nombre,email,password,foto)
        open_form('homepage.Empleados')
        #get_open_form().raise_event('x-refresh')
      else:  
        #anvil.alert(" el nombre indicado no existe y lo creo")
        #emp_row=anvil.server.call('creaCliente',nombre,email,estado,telefono,sueldo,sexo,cfisicaRow,dieta,direccion,ciudad,objetivo,diasVisita,horaVisita,horaVisita24,foto,birthday)
        #emp_row=anvil.server.call('creaEmpleado',codigo,nombre,email,estado,telefono,sueldo,frecPago,tipoPago,sexo,direccion,ciudad,foto,birthday)
        try:
          anvil.server.call('creaEmpleado',codigo,nombre,email,estado,telefono,sueldo,frecPago,tipoPago,sexo,direccion,ciudad,foto,birthday)
          password="123" #temporal
          #emp_row=anvil.server.call('creaUsuarioEmp',nombre,email,password,foto)
          anvil.server.call('creaUsuarioEmp',nombre,email,password,foto)
  
          anvil.alert(f"Employee {nombre} created!")
          open_form('homepage.Empleados')
        except anvil.server.AppOfflineError:
          anvil.alert("You're disconnected from Internet or Server is down!, please try later...")
    
  def text_box_nombre_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def text_box_tarifa_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def text_box_precio_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def radio_button_femenino_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    pass

  def button_cancel_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('homepage.Empleados')

  def drop_down_payfrec_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def drop_down_paytype_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def text_box_email_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def text_box_telefono_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass









