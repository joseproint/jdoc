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
    global sucursal,deposito,archivo,gaveta,seccion, ubiGlobal
    self.init_components(**properties)
    sucursal=''
    deposito=''
    archivo=''
    gaveta=''
    seccion=''
    ubiGlobal=''
    rowClases =  anvil.server.call('get_ClasesExpSql')
    rowCbienes = anvil.server.call('get_ClasesBienesSql')
    rowEstado = anvil.server.call('get_estadosBien')
    status='T'
    emp_rows = anvil.server.call('get_Empleados',status)
    self.llenaListas(rowClases,rowCbienes,rowEstado,emp_rows)

    #self.refresh()
    #self.set_event_handler("x-refresh", self.refresh)

    # Any code you write here will run before the form opens.

  #def refresh(self, **event_args):
    # self.repeating_panel_sucursales.items = anvil.server.call('get_Sucursales')
    #self.repeating_panel_expedientes.items = anvil.server.call("get_ExpedientesSql")

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
    suc="001"
    suc = self.dd_sucursal.selected_value
    global sucursal,deposito,archivo,gaveta,seccion,ubiGlobal
    sucursal=str(suc).zfill(3)
    #self.actUbicacion()
    ubiGlobal=f"{sucursal}%"
    sqlStr = self.lbl_sql.text
    if sqlStr is None or sqlStr=='':
      sqlStr=f" where ubicacion like '{ubiGlobal}'"
    else:
      sqlStr=f" {sqlStr} and ubicacion like '{ubiGlobal}'"
    self.lbl_sql.text = sqlStr
    self.link_ubicacion.icon='fa:check'
    
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
    ## status = self.drop_down_status.selected_value
    ## status=self.realStatus(status)
    #codigo=self.text_box_codigo.text
    #etiqueta=self.txt_etiqueta.text
    #descripcion=self.text_box_descripcion.text
    #claseXpediente = self.dd_clases.selected_value
    #clasePropiedad = self.dd_clasesBienes.selected_value
    #estadoPropiedad = self.dd_estado.selected_value
    ##usuario=self.drop_down_empleados.selected_value
    #self.actUbicacion()
    #ubicacion=ubiGlobal
    ##codigo=f"%{codigo}%"
    ##descripcion=f"%{descripcion}%"
    #whereStr=''
    #if etiqueta is not None and etiqueta!='':
    #  whereStr = f" where etiqueta='%{etiqueta}%'"
    #elif ubicacion is not None and ubicacion!='':
    #  whereStr = f" where ubicacion='{ubicacion}'"
    #elif codigo is not None and codigo !='':
    #  whereStr = f" where id like '%{codigo}%'"
    #elif descripcion is not None and descripcion!='':
    #  whereStr = f" where decripcion like '%{descripcion}%'"
    #else:
    #  if claseXpediente is not None:
    #    whereStr = f" where clase='{claseXpediente}'"
    #    if clasePropiedad is not None:
    #      if whereStr!='':
    #        whereStr = f" {whereStr} and claseBien='{clasePropiedad}'"
    #      else:
    #        whereStr = f" where claseBien='{clasePropiedad}'"
    #      if estadoPropiedad is not None:
    #        if whereStr!='':
    #          whereStr = f" {whereStr} and estadoBien='{estadoPropiedad}'"
    #        else:
    #          whereStr = f" where estadoBien='{estadoPropiedad}'"
    whereStr = self.lbl_sql.text        
    self.repeating_panel_expedientes.items = anvil.server.call(
      "searchDeep_Expedientes", whereStr
    )

  def dd_clases_change(self, **event_args):
    """This method is called when an item is selected"""
    claseExp = self.dd_clases.selected_value
    sqlStr = self.lbl_sql.text
    if sqlStr is None or sqlStr=='':
      sqlStr=f" where clase='{claseExp}'"
    else:
      sqlStr=f" {sqlStr} and clase='{claseExp}'"
    self.lbl_sql.text = sqlStr
    self.link_claseXp.icon='fa:check'
    
  def dd_estado_change(self, **event_args):
    """This method is called when an item is selected"""
    estadoExp = self.dd_estado.selected_value
    sqlStr = self.lbl_sql.text
    if sqlStr is None or sqlStr=='':
      sqlStr=f" where estadoBien='{estadoExp}'"
    else:
      sqlStr=f" {sqlStr} and estadoBien='{estadoExp}'"
    self.lbl_sql.text = sqlStr
    self.link_estadoBien.icon='fa:check'

  def dd_clasesBienes_change(self, **event_args):
    """This method is called when an item is selected"""
    claseBien = self.dd_clasesBienes.selected_value
    sqlStr = self.lbl_sql.text
    if sqlStr is None or sqlStr=='':
      sqlStr=f" where claseBien='{claseBien}'"
    else:
      sqlStr=f" {sqlStr} and claseBien='{claseBien}'"
    self.lbl_sql.text = sqlStr
    self.link_clasePropiedad.icon='fa:check'

  def btn_limpiar_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.lbl_sql.text=''
    self.repeating_panel_expedientes.items=[]
    self.link_claseXp.icon=''
    self.link_estadoBien.icon=''
    self.link_clasePropiedad.icon=''
    self.link_ubicacion.icon=''
    self.dd_clases.selected_value='Cdeposito'
    self.dd_clasesBienes.selected_value='Apartamento'
    self.dd_estado.selected_value='Disponible'
    self.dd_sucursal.selected_value='001'
    
