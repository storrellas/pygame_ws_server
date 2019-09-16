#!/usr/bin/env python

import threading
import pygame
import sys


############ PY GAME ########################

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Set height/width and margin for segment
segment_width = 15
segment_height = 15
segment_margin = 3
 
#Velocidad inicial
cambio_x = segment_width + segment_margin
cambio_y = 0

class Segment(pygame.sprite.Sprite):
    """ 
    Segment in the snake
    """

    def __init__(self, x, y):
        # Super
        super().__init__()
          
        # Set height and width
        self.image = pygame.Surface([segment_height, segment_width])
        self.image.fill(WHITE)
  
        # Set start point
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


pantalla = None
sprite_list = None
snake_segments = []
def pygame_init():
    global pantalla
    global sprite_list
    # Inicializamos Pygame
    pygame.init()
    
    # Creamos una pantalla de 800x600
    pantalla = pygame.display.set_mode([800, 600])
    
    # Creamos un título para la ventana
    pygame.display.set_caption('Snake')
    
    sprite_list = pygame.sprite.Group()
    
    # Creamos la serpiente inicial.
    for i in range(15):
        x = 250 - (segment_height + segment_margin) * i
        y = 30
        segment = Segment(x, y)
        snake_segments.append(segment)
        sprite_list.add(segment)
    
    
import base64
from io import StringIO

import time


encodedStr = "Empty"
def game_forever():
    global snake_segments
    global sprin
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
                    cambio_x = (segment_height + segment_margin) * -1
                    cambio_y = 0
                if evento.key == pygame.K_RIGHT:
                    cambio_x = (segment_height + segment_margin)
                    cambio_y = 0
                if evento.key == pygame.K_UP:
                    cambio_x = 0
                    cambio_y = (segment_height + segment_margin) * -1
                if evento.key == pygame.K_DOWN:
                    cambio_x = 0
                    cambio_y = (segment_height + segment_margin)
                        
        # Eliminamos el último segmento de la serpiente
        # .pop() este comando elimina el último objeto de una lista.
        segment_old = snake_segments.pop()
        sprite_list.remove(segment_old)
        
        # Determinamos dónde aparecerá el nuevo segmento
        x = snake_segments[0].rect.x + cambio_x
        y = snake_segments[0].rect.y + cambio_y
        segment = Segment(x, y)
        
        # Insertamos un nuevo segmento en la lista
        snake_segments.insert(0, segment)
        sprite_list.add(segment)
        
        # -- Dibujamos todo
        # Limpiamos la pantalla
        pantalla.fill(BLACK)
        
        sprite_list.draw(pantalla)
                
        # Actualizamos la pantalla
        pygame.display.flip()
        
        # Pausa
        reloj.tick(1)


        print("New image available")
        pygame.image.save(pantalla, "screenshot.jpeg")
        data = pygame.image.tostring(pygame.display.get_surface(), "RGB")

        # print(type(data))

        # # Standard Base64 Encoding

        encodedBytes = base64.b64encode(data)
        #encodedStr = str(encodedBytes, "utf-8")
        encodedStr = encodedBytes.decode("utf-8")

        # with open("Output.txt", "w") as text_file:
        #     text_file.write(encodedStr)
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
        # name="MyName"
        # greeting = f"Hello {name}!"

        #await websocket.send(greeting)
        # print(type(encodedStr))
        # print(encodedStr)
        #await websocket.send(encodedStr)
        #await websocket.send("iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==")

        with open("screenshot.jpeg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            print("-- Read --")
            if encoded_string != encodedStr:
                print("they are different")
            #print(type(encoded_string))
            await websocket.send(encoded_string.decode('utf-8'))
            #await websocket.send(encodedStr)

        #await websocket.send("MyNameIs")
        #print(f"> {greeting}")
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
pygame_init()
thread1 = threading.Thread(target=game_forever)
thread1.start()

# Websocket
start_server = websockets.serve(hello, "0.0.0.0", 7071)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
