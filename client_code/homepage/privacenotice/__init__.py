from ._anvil_designer import privacenoticeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..logo import Globals

class privacenotice(privacenoticeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_back_click(self, **event_args):
    """This method is called when the link is clicked"""
    #open_form('homepage.autor')
    #lasform=anvil.server.call('f_getLastform')
    lastform = Globals.f_getLastform()
    open_form(lastform)

