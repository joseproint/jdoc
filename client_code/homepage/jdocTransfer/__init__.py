from ._anvil_designer import jdocTransferTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import hpGlobals
from ..logo import Globals
import json
import time
import datetime
global server_time

class jdocTransfer(jdocTransferTemplate):
  def __init__(self, rowAF, **properties):
    #def __init__(self, rowAF, **properties):
    # Set Form properties and Data Bindings.
    #
    self.init_components(**properties)
    self.rowAF = rowAF
    #suc_rows = anvil.server.call('get_Sucursales')
    #suc_lista= [(s['sucNombre'],s) for s in suc_rows]
    #self.drop_down_loc.items = sorted(list(set(suc_lista)))
    ##self.drop_down_loc.items = suc_lista
    
    #self.locname=''
    #self.depname=''
    
    #dep_rows = anvil.server.call('get_departamentos')
    #dep_lista= [(d['nombre'],d) for d in dep_rows]
    ##self.drop_down_loc.items = sorted(list(set(dep_lista)))
    #self.drop_down_dep.items = dep_lista

    status='T'
    emp_rows = anvil.server.call('get_Empleados',status)
    emp_lista= [(r['empNombre'],r['empEmail']) for r in emp_rows]
    #self.drop_down_empleados.items = sorted(list(set(emp_lista)))
    self.drop_down_empleados.items = emp_lista
    # Any code you write here will run before the form opens.

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.expedientes')

  #def drop_down_loc_change(self, **event_args):
  #  """This method is called when an item is selected"""
  #  loc=self.drop_down_loc.selected_value
  #  self.loc=loc['sucID']
  #  self.locname=loc['sucNombre']
  #  print(f"loc:{loc['sucID']} - {loc['sucNombre']}")

  #def drop_down_dep_change(self, **event_args):
  #  """This method is called when an item is selected"""
  #  depto=self.drop_down_dep.selected_value
  #  self.depto=depto['depto'] #guardo el codigo del depto
  #  self.depname=depto['nombre']

  #def drop_down_responsible_change(self, **event_args):
  #  """This method is called when an item is selected"""
  #  empleado=self.drop_down_empleados.selected_value
  #  self.empleado=empleado['empCodigo']
  #  self.empname=empleado['empNombre']

  def btn_guardar_click(self, **event_args):
    """This method is called when the button is clicked"""
    global server_time
    fRetorno=self.fechaRetorno.date
    etiqueta=self.rowAF.text_box_codigo.text

    #loc=self.drop_down_loc.selected_value
    #self.loc=loc['sucID']
    #locname=self.locname
    #depname=self.depname

    #depto=self.drop_down_dep.selected_value
    #self.depto=depto['depto'] #guardo el codigo del depto
    #depto=self.depto
    ##depname=depto['nombre']
    
    empleado=self.drop_down_empleados.selected_value
    #alert(f"Empleado:{empleado}")
    #self.empleado=empleado['empCodigo']
    self.empleado=empleado
    codemp=self.empleado
    ##self.nombreemp=empleado['empNombre']
    #nombreemp=self.empname
    #nombreemp = empleado['empNombre']
    nombreemp = empleado
        
    #lat=hpGlobals.f_getLat()
    #lng=hpGlobals.f_getLng()
    notas=self.txt_notes.text
    firma=None
    cia=''
    #codigoaf=self.rowAF.codigoaf
    #descripcion=self.rowAF.descripcion
    codigoaf=etiqueta
    descripcion='?'
    
    self.loc=0
    self.lat=0
    self.lng=0
    self.depto=''
    locname=''
    depname=''
    
    server_time = anvil.server.call('ServerTimeZone')
    fecha = server_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    codExpediente=etiqueta
    empEntrega = Globals.f_getEmail()
    empRecibe = empleado
    
    #if anvil.server.call('transfiereExp',fecha,etiqueta,codigoaf,codemp,cia,self.loc,self.depto,self.lat,self.lng,firma,notas)==True:
    tipotrans='TRANSFERENCIA'
    numtrans=None
    esDevolucion=False
    if anvil.server.call('transfiereExp',fecha,codExpediente,empRecibe,empEntrega,notas,tipotrans,numtrans,fRetorno,esDevolucion) is True:
      #transferencia Ok
      #self.generaPDF(fecha,codExpediente,codExpediente,empRecibe,cia,locname,depname,self.lat,self.lng,firma,notas,descripcion)
      alert('transferencia realizada')
      open_form('homepage.expedientes')
    else:
      alert('transferencia no realizada')

  def generaPDF(self,fecha,etiqueta,codigoaf,codemp,cia,loc,depto,lat,lng,firma,notas,descripcion):
    import anvil.media
    pantalla='Transferencia EXP'
    #print("a generar pdf")
    #pdf = anvil.server.call('createSend_pdf',pantalla,fecha,etiqueta,codigoaf,codemp,cia,loc,depto,lat,lng,firma,notas,descripcion)
    #anvil.media.download(pdf)
    pdf=None
    #===============> envio el pdf por enail <===================
    #origen=anvil.server.call('f_CoachRowID')
    origen=Globals.f_getEmail()
    empDestino=self.drop_down_empleados.selected_value
    nombreEmp=anvil.server.call('f_nombreEmpleado',empDestino)
    nombreOrigen=anvil.server.call('f_nombreEmpleado',origen)
    #destino=anvil.server.call('f_emailEmpSql',empDestino)
    destino=empDestino
    titulo='Transferencia de Expediente - Plataforma jDoc'
    notas=f"""
      
      Estimado {nombreEmp},
      Por medio de la presente hacemos de su conocimiento la transferencia del Expediente No. {etiqueta}, la fecha de retorno es {fecha}
      Saludos cordiales,

      {nombreOrigen}
    """
    #task=anvil.server.call('fEmailTask',origen,destino,titulo,notas,pdf)
    #print(task)

  def drop_down_responsible_change(self, **event_args):
    """This method is called when an item is selected"""
    pass
  