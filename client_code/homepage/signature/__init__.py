from ._anvil_designer import signatureTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files


class signature(signatureTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_save_click(self, **event_args):
    """This method is called when the button is clicked"""
    url=URLMedia(self.call_js('getURL'))
    self.image_1.source = url

  def button_clear_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.call_js('clear')

  def link_atras_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.jdocTransfer')
