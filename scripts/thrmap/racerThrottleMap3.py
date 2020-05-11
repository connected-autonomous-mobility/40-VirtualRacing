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
from math import sqrt
from docopt import docopt
import tensorflow.python.keras as keras
from PIL import Image


thrMap = np.genfromtxt('ThrottleMap.csv',delimiter=',')
global lastPos
lastPos = 0

# Server port
PORT = 9091
IMG_NORM_SCALE = 1.0 / 255.0

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
        global lastPos
        self.EOLflag = False
        

    def on_msg_recv(self, json_packet):

        global lastPos

        if json_packet['msg_type'] == "car_loaded":
            self.car_loaded = True
        
        if json_packet['msg_type'] == "telemetry":
            imgString = json_packet["image"]
            image = Image.open(BytesIO(base64.b64decode(imgString)))
            self.last_image = np.asarray(image).astype(np.float32) * IMG_NORM_SCALE

            self.cte = json_packet["cte"]
            self.speed = json_packet["speed"]
            self.strAngle = json_packet["steering_angle"]
            self.thrPos = json_packet["throttle"]
            self.pos_x = json_packet["pos_x"]
            self.pos_y = json_packet["pos_y"]
            self.pos_z = json_packet["pos_z"]
            
            #simplotWriter.writerow([self.pos_x, self.pos_y, self.pos_z, self.cte, self.strAngle, self.thrPos, self.speed])

            self.lastX = thrMap[lastPos,1]
            self.lastZ = thrMap[lastPos,3]
            self.minDistance = sqrt((self.pos_x-self.lastX)**2 + (self.pos_z-self.lastZ)**2)
            
            i = 0

            for i in range(lastPos, 255):
                self.newX = thrMap[i,1]
                self.newZ = thrMap[i,3]
                self.newDistance = sqrt((self.pos_x-self.newX)**2 + (self.pos_z-self.newZ)**2)
                if self.newDistance <= self.minDistance:
                    self.minDistance = self.newDistance
                    #self.lastPosition = i
                    #print(i)
                    if(i > 253):
                        print('Flag!!')
                        self.EOLflag = True
                        lastPos = 0
                        break
                else:
                    #self.lastPosition = max(i-1, 0)
                    lastPos = max(i-1, 0)
                    break
                i += 1
            '''
            if self.EOLflag:
                print('New Lap!!')
                self.lastPosition = 0
                self.EOLflag = False
                for i in range(lastPos, 255):
                    self.newX = thrMap[i,1]
                    self.newZ = thrMap[i,3]
                    self.newDistance = sqrt((self.pos_x-self.newX)**2 + (self.pos_z-self.newZ)**2)
                    if self.newDistance <= self.minDistance:
                        self.minDistance = self.newDistance
                        #self.lastPosition = i
                        #print(i)
                        if(i == 255):
                            self.EOLflag = True
                    else:
                        #self.lastPosition = max(i-1, 0)
                        lastPos = max(i-1, 0)
                        break
                    i += 1
            '''
    def send_controls(self, steering, throttle):
        p = { "msg_type" : "control",
                "steering" : steering.__str__(),
                "throttle" : throttle.__str__(),
                "brake" : "0.0" }
        msg = json.dumps(p)
        self.send(msg)

    def update(self):

        global lastPos


        if self.last_image is not None:
            outputs = self.model.predict(self.last_image[None, :, :, :])
            steering = outputs[0][0][0]
            throttle = outputs[1][0][0]

            #self.targetSpeed = thrMap[lastPos, 8] * 0.9999 ### rbx ###
            self.targetSpeed = thrMap[lastPos, 8] 
            print(thrMap[lastPos, 8])
            if self.speed < self.targetSpeed:
                if self.targetSpeed == 30:
                    throttle = 1.0
                else:
                    throttle = 0.50
            elif self.speed > self.targetSpeed:
                if self.speed > 13:
                    throttle = -1.0
                    steering = 0.0
                else:    
                    throttle = -0.1
            else:
                throttle = 0.25

            if lastPos < 20:
                if self.speed < 8.0:
                    if self.cte > -2.25:
                        #steering = -0.1
                        steering = -0.05
                        throttle = 1.0

            #print(lastPos, self.speed, steering,throttle)
            self.send_controls(steering, throttle)


def race(model_path, host, name):

    # Load keras model
    model = keras.models.load_model(model_path)

    # Create client
    client = RaceClient(model, (host, PORT))

    # load scene
    msg = '{ "msg_type" : "load_scene", "scene_name" : "generated_track" }'
    client.send(msg)
    time.sleep(1.0)

    # Car config
    msg = '{ "msg_type" : "car_config", "body_style" : "car01", "body_r" : "128", "body_g" : "0", "body_b" : "128", "car_name" : "%s", "font_size" : "40" }' % (name)
    client.send(msg)
    time.sleep(0.2)

    try:
        while True:
            client.update()
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    client.stop()

if __name__ == '__main__':
    args = docopt(__doc__)
    race(model_path = args['--model'], host = args['--host'], name = args['--name'])
