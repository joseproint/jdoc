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

  def link_ubicaciones_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.sucursales')

  def link_clasesexp_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.clasesexp')

  def link_clasesExp_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.clasesexp')

  def link_expedientes_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.expedientes')

  def link_transferencia_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.jdocTransfer', self)

  def link_clasebien_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.clasesbienes')

  def link_mapa_click(self, **event_args):
    """This method is called when the link is clicked"""
    #alert('en construccion..')
    open_form('homepage.mapa')

  def link_vencimientos_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.retVencidos')

  def link_invDoc_click(self, **event_args):
    """This method is called when the link is clicked"""
    #open_form('homepage.jassetinvcheck')
    pass

