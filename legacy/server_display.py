#!/usr/bin/env python

import threading
import pygame
import sys


############ PY GAME ########################

# import os, sys

# # set SDL to use the dummy NULL video driver, 
# #   so it doesn't need a windowing system.
# os.environ["SDL_VIDEODRIVER"] = "dummy"

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Set height/width and margin for segment
segment_width = 15
segment_height = 15
segment_margin = 3
 
#Velocidad inicial
delta_x = segment_width + segment_margin
delta_y = 0

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


display = None
sprite_list = None
snake_segments = []
def pygame_init():
    global display
    global sprite_list
    # Initialise Pygame
    pygame.init()
    
    # Create a 800x600 display
    display = pygame.display.set_mode([800, 600])


    # # surface alone wouldn't work so I needed to add a rectangle
    # pygame.display.set_mode([1, 1])
    # display = pygame.Surface((800, 600), pygame.SRCALPHA, 32)
    # pygame.draw.rect(display, (0,0,0), (0, 0, 800, 600), 0)
    
    # Set title
    pygame.display.set_caption('Snake')
    
    sprite_list = pygame.sprite.Group()
    
    # Generate initial snake
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
    global delta_x
    global delta_y
    global encodedStr
    clock = pygame.time.Clock()
    done = False
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    
            # Set speed depending on the pressed key
            # We want speed to be enough to move a segment plus margin
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    delta_x = (segment_height + segment_margin) * -1
                    delta_y = 0
                if event.key == pygame.K_RIGHT:
                    delta_x = (segment_height + segment_margin)
                    delta_y = 0
                if event.key == pygame.K_UP:
                    delta_x = 0
                    delta_y = (segment_height + segment_margin) * -1
                if event.key == pygame.K_DOWN:
                    delta_x = 0
                    delta_y = (segment_height + segment_margin)
                        
        # Delete last segment in snake
        segment_old = snake_segments.pop()
        sprite_list.remove(segment_old)
        
        # Caltulate where to make it appear
        x = snake_segments[0].rect.x + delta_x
        y = snake_segments[0].rect.y + delta_y
        segment = Segment(x, y)
        
        # Insert new segment
        snake_segments.insert(0, segment)
        sprite_list.add(segment)
        
        # -- Clean display
        display.fill(BLACK)
        
        sprite_list.draw(display)
                
        # Update display
        pygame.display.flip()
        
        # Pause
        clock.tick(1)


        print("New image available")
        pygame.image.save(display, "screenshot.jpeg")
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
