from ._anvil_designer import jdocTransfer_copyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import hpGlobals
import json

class jdocTransfer_copy(jdocTransfer_copyTemplate):
  def __init__(self, fecha,etiqueta,codigoaf,codemp,cia,loc,depto,lat,lng,firma,notas,descripcion, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.rowAF = rowAF
    self.txt_date.text=fecha
    self.txt_labelcode.text=etiqueta
    self.txt_loc.text=loc
    self.txt_dep.text=depto
    self.txt_emp.text=codemp
    self.txt_notes.text=notas
    self.txt_afID.text=codigoaf
    self.txt_descripcion.text=descripcion

    row_usuario = anvil.server.call('fDatosUsuario')  
    ciaName=row_usuario['userCiaName']
    userName=row_usuario['userName']
    self.label_cia.text=ciaName
    self.txt_deliveredby.text=userName
