from ._anvil_designer import mainmenuTemplate
from anvil import *
import anvil.server


class mainmenu(mainmenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_autor_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.autor')

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage')

  def link_usuarios_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.Empleados')

  def link_sucursales_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.sucursales')
