from ._anvil_designer import expedientesTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class expedientes(expedientesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()
    self.set_event_handler('x-refresh', self.refresh)

    # Any code you write here will run before the form opens.

  def refresh(self, **event_args):
    #self.repeating_panel_sucursales.items = anvil.server.call('get_Sucursales')
    self.repeating_panel_expedientes.items = anvil.server.call('get_ClasesExpSql')
    
  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.mainmenu')

  def link_add_click(self, **event_args):
    """This method is called when the link is clicked"""
    descripcion=None
    sucRow=None
    open_form('homepage.expediente',descripcion,sucRow)



