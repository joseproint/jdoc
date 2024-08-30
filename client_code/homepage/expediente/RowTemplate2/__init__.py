from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_notas_click(self, **event_args):
    """This method is called when the link is clicked"""
    alert(f"Nota: {self.item['notas']}")

  def link_origen_click(self, **event_args):
    """This method is called when the link is clicked"""
    userOrigen=self.item['empEntrega']
    alert(f"Usuario:{userOrigen}")

  def link_destino_click(self, **event_args):
    """This method is called when the link is clicked"""
    userDestino=self.item['empRecibe']
    alert(f"Usuario:{userDestino}")
