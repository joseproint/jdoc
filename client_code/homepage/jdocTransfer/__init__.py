from ._anvil_designer import jdocTransferTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import hpGlobals
from ..logo import Globals
import json

class jdocTransfer(jdocTransferTemplate):
  def __init__(self, **properties):
    #def __init__(self, rowAF, **properties):
    # Set Form properties and Data Bindings.
    #
    self.init_components(**properties)
    #self.rowAF = rowAF
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
    #emp_lista= [(r['empNombre'],r) for r in emp_rows]
    #self.drop_down_empleados.items = sorted(list(set(emp_lista)))
    self.drop_down_empleados.items = emp_rows
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
    fecha=self.fechaRetorno.date
    etiqueta=self.rowAF.txt_codigo.text

    #loc=self.drop_down_loc.selected_value
    #self.loc=loc['sucID']
    #locname=self.locname
    #depname=self.depname

    #depto=self.drop_down_dep.selected_value
    #self.depto=depto['depto'] #guardo el codigo del depto
    #depto=self.depto
    ##depname=depto['nombre']
    
    empleado=self.drop_down_empleados.selected_value
    self.empleado=empleado['empCodigo']
    codemp=self.empleado
    #self.nombreemp=empleado['empNombre']
    nombreemp=self.empname
    
    #lat=hpGlobals.f_getLat()
    #lng=hpGlobals.f_getLng()
    notas=self.txt_notes.text
    firma=None
    cia=''
    codigoaf=self.rowAF.codigoaf
    descripcion=self.rowAF.descripcion

    self.loc=0
    self.lat=0
    self.depto=''
    locname=''
    depname=''
        
    if anvil.server.call('transfiereAF',fecha,etiqueta,codigoaf,codemp,cia,self.loc,self.depto,lat,lng,firma,notas)==True:
      #transferencia Ok
      alert('transferencia realizada')
      self.generaPDF(fecha,etiqueta,codigoaf,nombreemp,cia,locname,depname,lat,lng,firma,notas,descripcion)
    else:
      alert('transferencia no realizada')

  def generaPDF(self,fecha,etiqueta,codigoaf,codemp,cia,loc,depto,lat,lng,firma,notas,descripcion):
    import anvil.media
    pantalla='Transferencia AF'
    print("a generar pdf")
    pdf = anvil.server.call('createSend_pdf',pantalla,fecha,etiqueta,codigoaf,codemp,cia,loc,depto,lat,lng,firma,notas,descripcion)
    anvil.media.download(pdf)
    #===============> envio el pdf por enail <===================
    origen=anvil.server.call('f_CoachRowID')
    origen=Globals.f_getEmail()
    empDestino=self.drop_down_empleados.selected_value
    nombreEmp=empDestino['empNombre']
    destino=anvil.server.call('f_emailEmpSql',nombreEmp)
    titulo='Transferencia AF - jdoc Platform'
    notas=f"""
      
      Estimado {nombreEmp},
      Anexo enviamos formulario de transferencia del activo {descripcion}, la fecha de retorno es {fecha}
      Saludos cordiales,
      
    """
    task=anvil.server.call('fEmailTask',origen,destino,titulo,notas,pdf)
    print(task)
  