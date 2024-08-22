from ._anvil_designer import RowTemplate9Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate9(RowTemplate9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
  
    # Any code you write here will run before the form opens.

  def link_edit_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage.expediente',self.label_1.text, self.item )
    

  def link_delete_click(self, **event_args):
    """This method is called when the link is clicked"""
    delete_clicked = alert(f"Are you sure you want to delete {self.label_1.text}?",
                   large=True,
                   buttons=[("yes", True), ("Cancel", False)])
    if delete_clicked:
      nombreCexp = self.label_1.text #nombre
      anvil.server.call('deleteExpFromGridSql', self.item,nombreCexp)
      #anvil.server.call('delete_Cliente', self.text_box_email.text)
      get_open_form().raise_event('x-refresh')
