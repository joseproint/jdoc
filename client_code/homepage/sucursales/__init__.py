from ._anvil_designer import sucursalesTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class sucursales(sucursalesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()
    self.set_event_handler('x-refresh', self.refresh)

    # Any code you write here will run before the form opens.

  def refresh(self, **event_args):
    #self.repeating_panel_sucursales.items = anvil.server.call('get_Sucursales')
    self.repeating_panel_sucursales.items = anvil.server.call('get_SucursalesSql')
    
  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.mainmenu')

  def link_add_click(self, **event_args):
    """This method is called when the link is clicked"""
    descripcion=None
    sucRow=None
    open_form('homepage.sucursal',descripcion,sucRow)



