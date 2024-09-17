from ._anvil_designer import retVencidosTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files


class retVencidos(retVencidosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()
    self.set_event_handler('x-refresh', self.refresh)

    # Any code you write here will run before the form opens.

  def refresh(self, **event_args):
    #self.repeating_panel_sucursales.items = anvil.server.call('get_Sucursales')
    self.repeating_panel_retVencidos.items = anvil.server.call('get_ExpedientesSql')

  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.mainmenu')
    