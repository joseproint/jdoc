from ._anvil_designer import notasTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import base64

class notas(notasTemplate):
  def __init__(self, item, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.lbl_notas.text=item['notas']

    tipotrans='TRANSFERENCIA'
    numtrans = item['numtrans']
    columna = 'firma'
    firma = anvil.server.call('get_foto',tipotrans,numtrans,columna)
    if firma:
      #self.image_2.source=firma
      mime_type="image/jpg"
      binary_data = base64.b64decode(firma)
      media_Object=BlobMedia(mime_type, binary_data)
      self.image_firma.source=media_Object
    else:
      alert("Imagen firma no es válida..")

    #Ahora leo la foto de la cedula de identidad
    columna = 'cedula'
    cedula = anvil.server.call('get_foto',tipotrans,numtrans,columna)
    if cedula:
      #self.image_2.source=firma
      mime_type="image/jpg"
      binary_data = base64.b64decode(cedula)
      media_Object=BlobMedia(mime_type, binary_data)
      self.image_cedula.source=media_Object
    else:
      alert("Imagen Cedula de Identidad no es válida..")    
    # Any code you write here will run before the form opens.
