from ._anvil_designer import mapaTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files


class mapa(mapaTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    rowCbienes = anvil.server.call('get_ClasesBienesSql')
    rowEstado = anvil.server.call('get_estadosBien')
    self.dd_clasesBienes.items = [(r['descripcion'], r['id'].strip()) for r in rowCbienes]
    self.dd_estado.items = [r for r in rowEstado]
    # Any code you write here will run before the form opens.

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.mainmenu')
