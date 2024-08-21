from ._anvil_designer import EmpleadosTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Empleados(EmpleadosTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()
    self.set_event_handler('x-refresh', self.refresh)
    self.repeating_panel_empleados.set_event_handler('x-refresh', self.refresh)
    # Any code you write here will run before the form opens.

  def realStatus(self,status):
    if status=='' or status=='All' or status is None:
      status='T'
    elif status=='Inactive':
      status='I'
    elif status=='Active':
      status='A'
    elif status=='Hold':
      status='H'
    print('status: '+status)
    return status
   
  def refresh(self, **event_args):
    status=self.drop_down_status.selected_value
    status=self.realStatus(status)
    self.repeating_panel_empleados.items = anvil.server.call('get_Empleados',status)
    # Any code you write here will run before the form opens.

  def link_add_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.Empleado',None, self.item)

  def search(self, **event_args):
    status = self.drop_down_status.selected_value
    status=self.realStatus(status)
    self.repeating_panel_empleados.items = anvil.server.call(
      'search_Empleados',
      self.text_box_search.text, status
    )

  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.mainmenu')

  def text_box_search_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def drop_down_status_change(self, **event_args):
    """This method is called when an item is selected"""
    status=self.realStatus(self.drop_down_status.selected_value)
    self.repeating_panel_empleados.items = anvil.server.call(
      'search_Empleados', self.text_box_search.text, status
    )
    
