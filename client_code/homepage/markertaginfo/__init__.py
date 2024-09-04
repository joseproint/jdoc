from ._anvil_designer import markertaginfoTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..logo import Globals

class markertaginfo(markertaginfoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    datos=Globals.f_getLabel1()
    self.label_1.text=datos
    #pfin=datos.find('-')
    ##pfin=pfin * (-1)
    #codigo=datos[3:pfin]
    #print(f"pfin:{pfin} codigo final:{codigo}")
    #foto=anvil.server.call('get_foto',codigo)
    #self.image_1.source=foto
    
    ##self.image_1.source=foto
    ## Any code you write here will run before the form opens.

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    #if file != None:
    #  self.item['fotografia']=file
    #  self.image_1.source=file
    #else:
    #  anvil.alert('FileLoader is not working')
    pass
    