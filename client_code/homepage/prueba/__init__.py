from ._anvil_designer import pruebaTemplate
from anvil import *
import anvil.server


class prueba(pruebaTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    anvil.alert('Hola, este msg fue creado localmente...')