#!/usr/bin/env python

import threading
import pygame
import sys


############ PY GAME ########################

# --- Globales ---
# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
 
# Establecemos el largo y alto de cada segmento de la serpiente
largodel_segmento = 15
altodel_segmento = 15
# Margen entre cada segmento
margendel_segmento = 3
 
#Velocidad inicial
cambio_x = largodel_segmento + margendel_segmento
cambio_y = 0

class Segmento(pygame.sprite.Sprite):
    """ Clase que representa un segmento de la serpiente. """
    # -- Métodos
    #  Función constructor
    def __init__(self, x, y):
        # Llamada al constructor padre
        super().__init__()
          
        # Establecemos el alto y largo
        self.image = pygame.Surface([largodel_segmento, altodel_segmento])
        self.image.fill(BLANCO)
  
        # Establecemos como punto de partida la esquina superior izquierda.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

pantalla = None
listade_todoslos_sprites = None
segementos_dela_serpiente = []
def pygame_init():
    global pantalla
    global listade_todoslos_sprites
    # Inicializamos Pygame
    pygame.init()
    
    # Creamos una pantalla de 800x600
    pantalla = pygame.display.set_mode([800, 600])
    
    # Creamos un título para la ventana
    pygame.display.set_caption('Serpiente')
    
    listade_todoslos_sprites = pygame.sprite.Group()
    
    # Creamos la serpiente inicial.
    for i in range(15):
        x = 250 - (largodel_segmento + margendel_segmento) * i
        y = 30
        segmento = Segmento(x, y)
        segementos_dela_serpiente.append(segmento)
        listade_todoslos_sprites.add(segmento)
    
    
import base64
from io import StringIO

import time


encodedStr = None
def game_forever():
    global segementos_dela_serpiente
    global listade_todoslos_sprites
    global cambio_x
    global cambio_y
    global encodedStr
    reloj = pygame.time.Clock()
    hecho = False
    while not hecho:
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True
    
            # Establecemos la velocidad basándonos en la tecla presionada
            # Queremos que la velocidad sea la suficiente para mover un segmento
            # más el margen.
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    cambio_x = (largodel_segmento + margendel_segmento) * -1
                    cambio_y = 0
                if evento.key == pygame.K_RIGHT:
                    cambio_x = (largodel_segmento + margendel_segmento)
                    cambio_y = 0
                if evento.key == pygame.K_UP:
                    cambio_x = 0
                    cambio_y = (altodel_segmento + margendel_segmento) * -1
                if evento.key == pygame.K_DOWN:
                    cambio_x = 0
                    cambio_y = (altodel_segmento + margendel_segmento)
                        
        # Eliminamos el último segmento de la serpiente
        # .pop() este comando elimina el último objeto de una lista.
        segmento_viejo = segementos_dela_serpiente.pop()
        listade_todoslos_sprites.remove(segmento_viejo)
        
        # Determinamos dónde aparecerá el nuevo segmento
        x = segementos_dela_serpiente[0].rect.x + cambio_x
        y = segementos_dela_serpiente[0].rect.y + cambio_y
        segmento = Segmento(x, y)
        
        # Insertamos un nuevo segmento en la lista
        segementos_dela_serpiente.insert(0, segmento)
        listade_todoslos_sprites.add(segmento)
        
        # -- Dibujamos todo
        # Limpiamos la pantalla
        pantalla.fill(NEGRO)
        
        listade_todoslos_sprites.draw(pantalla)
                
        # Actualizamos la pantalla
        pygame.display.flip()
        
        # Pausa
        reloj.tick(1)

        #pygame.image.save(pantalla, "screenshot.jpeg")
        data = pygame.image.tostring(pygame.display.get_surface(), "RGB")
        print("New image available")
        print(type(data))

        # Standard Base64 Encoding

        encodedBytes = base64.b64encode(data)
        encodedStr = str(encodedBytes, "utf-8")
        # print(len(encodedBytes))
        # print(encodedBytes[1:10])
        # print(type(encodedBytes))
        # print(type(encodedStr))

        # print(type(encodedBytes))
        # print(type(encodedStr))

        # data = StringIO()
        # pygame.image.save(pygame.display.get_surface(), data)
        # #data = base64.b64encode(data.getvalue())
        # print(type(data))

############ PY GAME ########################


# WS server example

import asyncio
import websockets

async def hello(websocket, path):
    print("Entered ...")
    while True:
        print("New Image ...")
        print("+++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++")
        global encodedStr
        # name = await websocket.recv()
        # print(f"< {name}")
        name="MyName"

        greeting = f"Hello {name}!"

        #await websocket.send(greeting)
        # print(type(encodedStr))
        # print(encodedStr)
        #await websocket.send(encodedStr)
        await websocket.send("MyNameIs")
        print(f"> {greeting}")
        print("+++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++")
        time.sleep(2)


# #####################
# data = "abc123!?$*&()'-=@~"

# # Standard Base64 Encoding
# encodedBytes = base64.b64encode(data.encode("utf-8"))
# encodedStr = str(encodedBytes, "utf-8")

# print(type(data))
# print(type(data.encode("utf-8")))
# print(type(encodedBytes))
# print(type(encodedStr))
# sys.exit(0)
# #####################

# Launch separated thread
# pygame_init()
# thread1 = threading.Thread(target=game_forever)
# thread1.start()

# Websocket
start_server = websockets.serve(hello, "0.0.0.0", 7071)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
