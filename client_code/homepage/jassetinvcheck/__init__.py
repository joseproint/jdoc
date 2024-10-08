from ._anvil_designer import jassetinvcheckTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from .. import hpGlobals
import anvil.js
from anvil_extras.storage import indexed_db

global af_store
global codigos
global validar
global itemsFound,itemsLost,itemsRare,itemsMisplaced,loc,dep,totalAf,lat,lng

class jassetinvcheck(jassetinvcheckTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    global codigos
    global validar
    global itemsFound,itemsLost,itemsRare,itemsMisplaced,loc,dep,totalAf,afRows
    global lat,lng
    self.me_marker = None
    hpGlobals.f_setLat(None)
    hpGlobals.f_setLng(None)
    lat=0
    lng=0
    validar=True
    itemsFound=0
    itemsLost=0
    itemsRare=0
    itemsMisplaced=0
    totalAf=0
    #codigos=''
    codigos=[]
    afRows=[]
    #suc_rows = anvil.server.call('get_Sucursales')
    suc_rows = anvil.server.call('get_SucursalesSql')
    suc_lista= [(s['sucNombre'],s) for s in suc_rows]
    self.drop_down_loc.items = sorted(list(set(suc_lista)))
    #self.drop_down_loc.items = suc_lista
    #print(suc_rows)
    loc=self.drop_down_loc.selected_value['sucID']
    
    dep_rows = anvil.server.call('get_departamentos')
    dep_lista= [(d['nombre'],d) for d in dep_rows]
    #self.drop_down_loc.items = sorted(list(set(dep_lista)))
    self.drop_down_dep.items = dep_lista
    # Any code you write here will run before the form opens.
    dep=self.drop_down_dep.selected_value['depto']
    
  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('homepage')
    
  def drop_down_loc_change(self, **event_args):
    """This method is called when an item is selected"""
    global loc
    loc=self.drop_down_loc.selected_value['sucID']
    print(f"loc:{loc}")

  def txt_itemcode_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    global codigos
    global validar
    global itemsFound,itemsLost,itemsRare,itemsMisplaced,loc,dep,totalAf,afRows
    global lat,lng
    dato = self.txt_itemcode.text
    if self.get_key(dato)==1:
      #item ya fue scaneado
      #if len(dato)<=30:
      if len(dato)<=5:
        #aviso solo cuando leen codigos pequeños que entendemos son codigos de barra
        #pero no avisamos si son tags porque el scanner los lee en lote
        #alert(f"Item {dato} have been scanned!")
        pass
    else:      
      #item no ha sido scaneado
      codigos.append(dato)
      codigos.sort(reverse = True)

      self.drop_down_lista.items = codigos
      self.drop_down_lista.selected_value=dato
      self.txt_itemcode.text=''
      self.txt_itemcode.focus()
      if validar:
        #print(f"totalAf: {totalAf}")
        if totalAf==0:
          self.lbl_msg.visible=True #mensaje que estamos cargando datos desde la nube
          alert('voy a leer los activos indicados...')
          afRows=anvil.server.call('get_Afs',loc,dep)
          alert('terminé de leer los activos indicados...')
          #====> guardo datos en indexedDB <====
          #if indexed_db.is_available()==False:
          if not indexed_db.is_available():
            alert('Database not supported in this browser!')
          else:  
            alert('voy a crear basedatos local...')
            af_store = indexed_db.create_store('afDB')
            for  x in afRows:
               sucRow={'ID':x['ID'],'descripcion':x['descripcion'],'registro':x['registro'],'localidad':x['localidad'],'depto':x['depto'],'lat':x['lat'],'lng':x['lng'],'codEtiqueta':x['codEtiqueta'],'localidad_actual':x['localidad_actual'],'depto_actual':x['depto_actual']}
               af_store[x['ID']]=sucRow
            alert('basedatos local creada...')
          self.inicializaPerdidos(loc,dep)  
          totalAf=self.get_AfsDep(loc,dep)
          self.lbl_msg.visible=False
          itemsLost=totalAf
          #alert(f"itemsLost: {itemsLost}")
          sucRow = anvil.server.call('f_sucGeoCord',loc)
          if sucRow is not None:
            lat = sucRow['sucLat']
            lng = sucRow['sucLng']
          else:
            #busco coordenadas con el gps tomadas del componente geolocator_1
            lat=hpGlobals.f_getLat()
            lng=hpGlobals.f_getLng()
        print(f"lat:{lat} lng:{lng}")
        afRow=None
        afRow=self.get_activo(dato)
        if afRow is not None:
          #item encontrado en basedatos
          self.txt_description.text=afRow['descripcion']
          #print(f"loc:{loc} localidad:{afRow['localidad']} dep:{dep} depto:{afRow['depto']}")
          if loc == afRow['localidad'] and dep == afRow['depto']:
            itemsFound += 1
            itemsLost = itemsLost - 1
            indicador='F' #Found
            self.marcaAf(dato,indicador)    
          else:
            itemsMisplaced+=1
            #itemsLost = itemsLost - 1
            indicador='M' #Misplaced
            self.marcaAf(dato,indicador)
        else:
          #item no encontrado en basedatos
          itemsRare+=1 #Raro
        self.lbl_found.text=itemsFound
        self.lbl_lost.text=itemsLost
        self.lbl_rare.text=itemsRare
        self.lbl_misplaced.text=itemsMisplaced
        self.lbl_resultados.text=f"Found:{itemsFound} | Misplaced:{itemsMisplaced} | Lost:{itemsLost} | Rare:{itemsRare}"

  def inicializaPerdidos(self,loc,dep):
    global afRows
    for x in afRows:
      if x['localidad']==loc and x['depto']==dep:
        if x['registro']=='' or x['registro'] is None:
          x['registro']='L'
          x['localidad_actual']=loc
          x['depto_actual']=dep        
          
  def marcaAf(self,dato,indicador):
    global afRows,loc,dep, lat,lng
    for x in afRows:
      if dato==x['ID']:
        x['registro']=indicador
        x['localidad_actual']=loc
        x['depto_actual']=dep
        x['lat']=lat
        x['lng']=lng
        print(f"codigo:{x['ID']} marked as {indicador}!!")

  def get_activo(self, codigo):
    #buscan en la tabla en ram el registro del 
    #código indicado y lo devuelve
    global afRows
    for x in afRows:
      if codigo==x['ID']:
        return x

  def get_AfsDep(self,loc,dep):
    #cuenta en la tabla en ram los activos 
    #de la loc y dep indicados
    global afRows
    cont=0
    for x in afRows:
      if loc==x['localidad'] and dep==x['depto']:
        cont+=1
    return cont
    
  def link_process_click(self, **event_args):
    """This method is called when the link is clicked"""
    global codigos,afRows,loc,dep
    scannedRows=[]
    for x in afRows:
      if loc==x['localidad_actual'] and dep==x['depto_actual']:
        codigo=x['ID']
        scannedRows.append(x)
        alert(f"{x['descripcion']} Registro: {x['registro']}")
    alert(f"scannerRows: {len(scannedRows)}")    
    task=anvil.server.call('f_procesaInv',scannedRows)    
    alert('Fin del Proceso, inventario actualizado en los servidores...')
    self.link_clearlist_click()
    
  def drop_down_lista_change(self, **event_args):
    """This method is called when an item is selected"""
    codigo=self.drop_down_lista.selected_value
    print(codigo)

  def drop_down_dep_change(self, **event_args):
    """This method is called when an item is selected"""
    global dep
    dep=self.drop_down_dep.selected_value['depto']
    print(f"dep:{dep}")

  def link_clearlist_click(self, **event_args):
    """This method is called when the link is clicked"""
    global codigos
    global itemsFound,itemsLost,itemsRare,itemsMisplaced,loc,dep,totalAf, afRows
    save_clicked = alert(f"The items have been processed, are you sure you want to clean the list of scanned items?",
        large=True,
        buttons=[("yes", True), ("Cancel", False)])
    if save_clicked:
      codigos=[]
      self.drop_down_lista.items=codigos
      self.txt_itemcode.text=''
      self.txt_description.text=''
      itemsFound=0
      itemsLost=0
      itemsRare=0
      itemsMisplaced=0
      totalAf=0
      self.lbl_found.text='0'
      self.lbl_lost.text='0'
      self.lbl_rare.text='0'
      self.lbl_misplaced.text='0'
      self.lbl_resultados.text=''
      afRows=[]
      self.repeating_panel_1.items=[]
      alert('List has been cleared!')
  
  #def cb_validar_change(self, **event_args):
  #  """This method is called when this checkbox is checked or unchecked"""
  #  global validar
  #  if self.cb_validar.checked:
  #    validar=True
  #  else:
  #    validar=False

  def get_key(self,val):
    global codigos
    scaneados=len(codigos)
    if scaneados>0:
      for x in codigos:
        if val in x:
          return 1
    return 0

  def link_found_click(self, **event_args):
    indicador='F'  
    self.repeatPanelUpdate(indicador)  
    
  def link_misplaced_click(self, **event_args):
    indicador='M'  
    self.repeatPanelUpdate(indicador)  

  def link_lost_click(self, **event_args):
    indicador='L'
    self.repeatPanelUpdate(indicador)  

  def repeatPanelUpdate(self,indicador):
    global afRows,loc,dep
    foundRows=[]
    for x in afRows:
      codigo=x['ID']
      registro=x['registro']
      #print(f"codigo:{codigo}")
      #busco solo en la localidad y depto que esta trabajando
      if indicador!='L':
        if registro==indicador:
          print(f"codigo:{codigo} registro:{registro}")
          foundRows.append(x)
      else:
        #indicador es Lost (valor nulo en campo registro)
        if loc==x['localidad'] and dep==x['depto']: #para revisar solo los de la ubicación que estoy trabajando
          print(f"{loc}-{x['localidad']} {dep}-{x['depto']} registro:{registro}")
          if registro=='None' or registro=='L':
            print("registro is none")
            foundRows.append(x)
    lista=self.datoAjson(foundRows)
    #print(f"{indicador} List:{lista}")
    print(f"{indicador} List:{foundRows}")
    if lista is not None:
      jsonObj=json.loads(lista)
      self.repeating_panel_1.items=jsonObj
    
  def datoAjson(self,dataRow):
    cont=1
    jsonData=''
    for r in dataRow:
      if cont>1:
        dato=', {"ID": "'+f"{r['ID']}"+'", "descripcion": "'+f"{r['descripcion']}"+'", "registro": "'+f"{r['registro']}"+'", "codEtiqueta": "'+f"{r['codEtiqueta']}"+'"'+'}'
      else:  
        dato='{"ID": "'+f"{r['ID']}"+'", "descripcion": "'+f"{r['descripcion']}"+'", "registro": "'+f"{r['registro']}"+'", "codEtiqueta": "'+f"{r['codEtiqueta']}"+'"'+'}'
      jsonData = jsonData + dato 
      cont=cont+1
    jsonData='['+jsonData+']'
    return jsonData

  def geolocator_1_update_location (self, lat, lng, **event_args):
    # This method is called when the user's location is updated
    hpGlobals.f_setLat(lat)
    hpGlobals.f_setLng(lng)
    #if not self.me_marker:
    #  self.me_marker = GoogleMap.Marker(position=GoogleMap.LatLng(lat,lng))
    #  self.map_1.add_component(self.me_marker)
    #else:
    #  self.me_marker.position = GoogleMap.LatLng(lat,lng)
    #self.map_1.center = self.me_marker.position
    #self.map_1.zoom = 8

  def text_box_2_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

    