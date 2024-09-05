from ._anvil_designer import deepsearchTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global sucursal,deposito,archivo,gaveta,seccion, ubiGlobal

class deepsearch(deepsearchTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    rowClases =  anvil.server.call('get_ClasesExpSql')
    rowCbienes = anvil.server.call('get_ClasesBienesSql')
    rowEstado = anvil.server.call('get_estadosBien')
    status='T'
    emp_rows = anvil.server.call('get_Empleados',status)
    self.llenaListas(rowClases,rowCbienes,rowEstado,emp_rows)

    self.refresh()
    self.set_event_handler("x-refresh", self.refresh)

    # Any code you write here will run before the form opens.

  def refresh(self, **event_args):
    # self.repeating_panel_sucursales.items = anvil.server.call('get_Sucursales')
    self.repeating_panel_expedientes.items = anvil.server.call("get_ExpedientesSql")

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("homepage.expedientes")

  def link_Inicio_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("homepage.mainmenu")

  def llenaListas(self, rowClases, rowCbienes, rowEstado, emp_rows):
    self.dd_sucursal.items = [(f"Sucursal {r}",r) for r in range(1,101)]
    self.dd_deposito.items = [(f"Deposito {r}",r) for r in range(1,11)]
    self.dd_archivo.items = [(f"Archivo {r}",r) for r in range(1,21)]
    self.dd_gaveta.items = [(f"Gaveta {r}",r) for r in range(1,9)]
    self.dd_seccion.items = [(f"Seccion {r}", r) for r in range(1,21)]
    self.dd_clases.items = [(r['descripcion'], r['id'].strip()) for r in rowClases]
    self.dd_clasesBienes.items = [(r['descripcion'], r['id'].strip()) for r in rowCbienes]
    self.dd_estado.items = [r for r in rowEstado]
    emp_lista= [(r['empNombre'],r['empEmail']) for r in emp_rows]
    self.drop_down_empleados.items = emp_lista

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

  def actUbicacion(self):
    global sucursal,deposito,archivo,gaveta,seccion, ubiGlobal
    ubicacion=f"{sucursal}{deposito}{archivo}{gaveta}{seccion}"  
    #self.txt_ubicacion.text=ubicacion
    ubiGlobal = ubicacion

  def link_search_click(self, **event_args):
    """This method is called when the link is clicked"""
    # status = self.drop_down_status.selected_value
    # status=self.realStatus(status)
    codigo=self.text_box_codigo.text
    etiqueta=self.txt_etiqueta.text
    descripcion=self.text_box_descripcion.text
    claseXpediente = self.dd_clases.selected_value
    clasePropiedad = self.dd_clasesBienes.selected_value
    estadoPropiedad = self.dd_estado.selected_value
    usuario=self.drop_down_empleados.selected_value
    self.actUbicacion()
    ubicacion=ubiGlobal
    codigo=f"%{codigo}%"
    descricion=f"%{descripcion}%"
    if etiqueta!=None:
      whereStr = f" where etiqueta='{etiqueta}'"
    elif ubicacion!=None:
      whereStr = f" where ubicacion='{ubicacion}'"
    elif codigo!=None:
      whereStr = f" where id like {codigo}"
    elif descripcion!=None:
      whereStr = f" where decripcion like {descripcion}"
    else:
      if claseXpediente!=None:
        whereStr = f" where clase='{claseXpediente}'"
        if clasePropiedad!=None:
          whereStr = f" and claseBien='{clasePropiedad}'"
          if estadoPropiedad!=None:
            whereStr = f" and estadoBien='{estadoPropiedad}'"
    self.repeating_panel_expedientes.items = anvil.server.call(
      "searchDeep_Expedientes", whereStr
    )

