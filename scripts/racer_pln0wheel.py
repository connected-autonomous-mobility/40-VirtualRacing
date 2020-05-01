"""
Script to drive a keras TF model with the Virtual Race Environment.

Usage:
    racer.py (--model=<model>) (--host=<ip_address>) (--name=<car_name>)
    
Options:
    -h --help        Show this screen.
"""

import os
import numpy as np
import json
import time
from io import BytesIO
import base64
import re
import socket
import select
from threading import Thread

from docopt import docopt
import tensorflow.python.keras as keras
from PIL import Image

import gui
import pygame

from influxdb import InfluxDBClient

import json
import datetime

#https://code-maven.com/serialize-datetime-object-as-json-in-python 
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

FR = 30
SIZE = 640, 480
BGCOLOR = (50,50,50)
NODECOLOR = (255,255,0)
NODESIZE = 5,5
GRIDSPACING = 50
MAXTRIES = 1000
STARTINGNODES = 8

# http://inventwithpython.com/pygame/chapter6.html
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = DARKGRAY

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
##DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Server port
PORT = 9091
IMG_NORM_SCALE = 1.0 / 255.0


def race_monitor(json_packet):
    global istep
    global dbclient
    global databasename

    print(json_packet)
    print("*** saving racing json_packet ***")
    ##SCREEN.fill(BGCOLOR)
    #print(json_packet["wheelEncoder1"],json_packet["wheelEncoder2"],json_packet["wheelEncoder3"],json_packet["wheelEncoder4"])
    
    #https://www.pygame.org/docs/ref/draw.html#pygame.draw.lines
    dx = 1
    dy = 10
    xoff = 100
    yoff = 400
    '''
    score = json_packet["wheelEncoderLR"]
    scoreSurf = BASICFONT.render('wheel encoder #1: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (120, 10)
    #scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    '''
    '''
    if istep == 0:
        point2 = [int(0+xoff),int(0+yoff)]
    point1 =[int(istep*dx+xoff), int(score*dy+yoff)]
    pygame.draw.aaline(SCREEN, RED, False, point1, point2)
    point2 = point1

    DISPLAYSURF.blit(scoreSurf, scoreRect)
    '''
    #json_timepacket={}
    #json_timepacket['date'] = datetime.datetime.now()
    #json_timebody = json.dumps(json_timepacket, default = myconverter)

    json_body = json_packet

    print(json_body)
    #json_body = json.dumps(json_packet, default = myconverter)
    
    #json_body = [{'msg_type': 'telemetry', 'steering_angle': -0.1100858, 'throttle': 0.3668642, 'speed': 1.031223, 'image': '', hit': 'none', 'pos_x': 49.69151, 'pos_y': 0.5551119, 'pos_z': 48.38097, 'acc_x': -0.07776082, 'acc_y': 0.04289941, 'acc_z': 0.8601844, 'ang_acc_x': 0.2617902, 'ang_acc_y': -1.297674, 'ang_acc_z': 0.1142441, 'wheelEncoder1': 0.8388807, 'wheelEncoder2': 0.936206, 'wheelEncoder3': 0.8862848, 'wheelEncoder4': 0.7989971, 'time': 573.8032, 'cte': 0.00151062}]
    #print(json_body)
    #https://www.influxdata.com/blog/writing-data-to-influxdb-with-python/
    #dbclient.write_points(json_body, database=databasename, time_precision='ms', batch_size=1, protocol='line')
    #dbclient.write_points(loginEvents)



def replace_float_notation(string):
    """
    Replace unity float notation for languages like
    French or German that use comma instead of dot.
    This convert the json sent by Unity to a valid one.
    Ex: "test": 1,2, "key": 2 -> "test": 1.2, "key": 2

    :param string: (str) The incorrect json string
    :return: (str) Valid JSON string
    """
    regex_french_notation = r'"[a-zA-Z_]+":(?P<num>[0-9,E-]+),'
    regex_end = r'"[a-zA-Z_]+":(?P<num>[0-9,E-]+)}'

    for regex in [regex_french_notation, regex_end]:
        matches = re.finditer(regex, string, re.MULTILINE)

        for match in matches:
            num = match.group('num').replace(',', '.')
            string = string.replace(match.group('num'), num)
    return string


class SDClient:
    def __init__(self, host, port, poll_socket_sleep_time=0.05):
        self.msg = None
        self.host = host
        self.port = port
        self.poll_socket_sleep_sec = poll_socket_sleep_time

        # the aborted flag will be set when we have detected a problem with the socket
        # that we can't recover from.
        self.aborted = False
        self.connect()


    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connecting to the server 
        print("connecting to", self.host, self.port)
        self.s.connect((self.host, self.port))

        # time.sleep(pause_on_create)
        self.do_process_msgs = True
        self.th = Thread(target=self.proc_msg, args=(self.s,))
        self.th.start()        


    def send(self, m):
        self.msg = m


    def on_msg_recv(self, j):
        # print("got:", j['msg_type'])
        # we will always have a 'msg_type' and will always get a json obj
        pass


    def stop(self):
        # signal proc_msg loop to stop, then wait for thread to finish
        # close socket
        self.do_process_msgs = False
        self.th.join()
        self.s.close()


    def proc_msg(self, sock):
        '''
        This is the thread message loop to process messages.
        We will send any message that is queued via the self.msg variable
        when our socket is in a writable state. 
        And we will read any messages when it's in a readable state and then
        call self.on_msg_recv with the json object message.
        '''
        sock.setblocking(0)
        inputs = [ sock ]
        outputs = [ sock ]
        partial = []

        while self.do_process_msgs:
            # without this sleep, I was getting very consistent socket errors
            # on Windows. Perhaps we don't need this sleep on other platforms.
            time.sleep(self.poll_socket_sleep_sec)

            try:
                # test our socket for readable, writable states.
                readable, writable, exceptional = select.select(inputs, outputs, inputs)

                for s in readable:
                    # print("waiting to recv")
                    try:
                        data = s.recv(1024 * 64)
                    except ConnectionAbortedError:
                        print("socket connection aborted")
                        self.do_process_msgs = False
                        break
                    
                    # we don't technically need to convert from bytes to string
                    # for json.loads, but we do need a string in order to do
                    # the split by \n newline char. This seperates each json msg.
                    data = data.decode("utf-8")
                    msgs = data.split("\n")

                    for m in msgs:
                        if len(m) < 2:
                            continue
                        last_char = m[-1]
                        first_char = m[0]
                        # check first and last char for a valid json terminator
                        # if not, then add to our partial packets list and see
                        # if we get the rest of the packet on our next go around.                
                        if first_char == "{" and last_char == '}':
                            # Replace comma with dots for floats
                            # useful when using unity in a language different from English
                            m = replace_float_notation(m)
                            j = json.loads(m)
                            self.on_msg_recv(j)
                        else:
                            partial.append(m)
                            if last_char == '}':
                                if partial[0][0] == "{":
                                    assembled_packet = "".join(partial)
                                    assembled_packet = replace_float_notation(assembled_packet)
                                    j = json.loads(assembled_packet)
                                    self.on_msg_recv(j)
                                else:
                                    print("failed packet.")
                                partial.clear()
                        
                for s in writable:
                    if self.msg != None:
                        # print("sending", self.msg)
                        s.sendall(self.msg.encode("utf-8"))
                        self.msg = None
                if len(exceptional) > 0:
                    print("problems w sockets!")

            except Exception as e:
                print("Exception:", e)
                self.aborted = True
                self.on_msg_recv({"msg_type" : "aborted"})
                break


class RaceClient(SDClient):
    

    def __init__(self, model, address, poll_socket_sleep_time=0.01):
        super().__init__(*address, poll_socket_sleep_time=poll_socket_sleep_time)
        self.last_image = None
        self.car_loaded = False
        self.model = model

    def on_msg_recv(self, json_packet):

        if json_packet['msg_type'] == "car_loaded":
            self.car_loaded = True
        
        if json_packet['msg_type'] == "telemetry":
            imgString = json_packet["image"]
            image = Image.open(BytesIO(base64.b64decode(imgString)))
            self.last_image = np.asarray(image).astype(np.float32) * IMG_NORM_SCALE
            
            json_packet["image"] = "23"
            myjson = json_packet
            #print(json_packet["wheelEncoderLR"],json_packet["wheelEncoderFL"],json_packet["wheelEncoderFR"],json_packet["wheelEncoderRR"])
            race_monitor(myjson)
            
    def send_controls(self, steering, throttle):
        p = { "msg_type" : "control",
                "steering" : steering.__str__(),
                "throttle" : throttle.__str__(),
                "brake" : "0.0" }
        msg = json.dumps(p)
        self.send(msg)

    def update(self):
        if self.last_image is not None:
            outputs = self.model.predict(self.last_image[None, :, :, :])
            steering = outputs[0][0][0]
            throttle = outputs[1][0][0]
            self.send_controls(steering, throttle)

def race(model_path, host, name):

    global istep

    # Load keras model
    model = keras.models.load_model(model_path)

    # Create client
    client = RaceClient(model, (host, PORT))

    # load scene
    msg = '{ "msg_type" : "load_scene", "scene_name" : "generated_track" }'
    client.send(msg)
    time.sleep(1.0)

    # Car config
    msg = '{ "msg_type" : "car_config", "body_style" : "dokney", "body_r" : "64", "body_g" : "64", "body_b" : "64", "car_name" : "%s", "font_size" : "100" }' % (name)
    client.send(msg)
    time.sleep(0.2)

    try:
        while True:
            client.update()
            time.sleep(0.1)
            istep += 1
            
            '''
            pygame.event.pump()
            # Exit the mainloop at any time the "ESC" key is pressed
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                break
            pygame.display.flip()
            pygame.time.delay(FR)
            '''
    except KeyboardInterrupt:
        pass

    client.stop()

if __name__ == '__main__':
    global SCREEN
    global istep # time step
    global dbclient
    global databasename
    istep = 0

    # setup influxdb
    databasename = "opnsense"
    dbclient = InfluxDBClient("127.00.0.1", 8086, "opnsense", "wurz", databasename)
    dbclient.create_database(databasename)

    ##pygame.init()
    ##BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    #SCREEN = pygame.display.set_mode(SIZE)
    ##SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    ##pygame.display.set_caption('Parking Lot Nerds - Racing Monitor')
    

    args = docopt(__doc__)
    race(model_path = args['--model'], host = args['--host'], name = args['--name'])

    ##pygame.quit()