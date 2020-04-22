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

import cv2
import matplotlib.pyplot as plt

class ArrowKeyboardControls:
    '''
    kind of sucky control, only one press active at a time. 
    good enough for a little testing.
    requires that you have an CvImageView open and it has focus.
    '''
    def __init__(self):
        self.left = 2424832
        self.right = 2555904
        self.up = 2490368
        self.down = 2621440
        self.codes = [self.left, self.right, self.down, self.up]
        self.vec = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def run(self):
        code = cv2.waitKeyEx(delay=100)
        for iCode, keyCode in enumerate(self.codes):
            if keyCode == code:
                return self.vec[iCode]
        return (0., 0.)


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
        self.myspeed = 0 # rbx
        self.mylastspeed = 0 # rbx
        #plt.figure()
        #plt.title('Parking Lot Nerds - Race Monitor')
        
    def on_msg_recv(self, json_packet):

        if json_packet['msg_type'] == "car_loaded":
            self.car_loaded = True
        
        if json_packet['msg_type'] == "telemetry":
            imgString = json_packet["image"]
            
            # pln
            myspeed    = json_packet["speed"]
            mythrottle = json_packet["throttle"]
            mysteering = json_packet["steering_angle"]
            myx        = json_packet["pos_x"]
            myy        = json_packet["pos_y"]
            myz        = json_packet["pos_z"]
            cte        = json_packet["cte"]
            #print(myspeed) #-mythrottle*mysteering)
            self.mylastspeed = self.myspeed
            self.myspeed = myspeed

           
            '''
            # Plot
            #plt.scatter(pos_pos_xs, pos_pos_zs, c=colors, alpha=0.5)
            plt.scatter(myx, myz, s=30, c=pos_speeds)
            
            plt.plot(myx, myz, c=colors, alpha=0.5)
            plt.xlim(-20,100)
            plt.ylim(-20,100)
            
            plt.title('Parking Lot Nerds - Recorded Tracks')
            plt.xlabel('x')
            plt.ylabel('z')
            plt.legend()
            
            plt.show()
            '''
            # pln

            image = Image.open(BytesIO(base64.b64decode(imgString)))
            self.last_image = np.asarray(image).astype(np.float32) * IMG_NORM_SCALE

            #plt.imshow(image)
            #plt.show()  # display it

    def send_controls(self, steering, throttle):
        p = { "msg_type" : "control",
                "steering" : steering.__str__(),
                "throttle" : throttle.__str__(),
                "brake" : "0.0" }
        msg = json.dumps(p)
        self.send(msg)

    def update0(self):
        if self.last_image is not None:
            outputs = self.model.predict(self.last_image[None, :, :, :])
            steering = outputs[0][0][0]
            throttle = outputs[1][0][0]
            self.send_controls(steering, throttle)

    def update(self): # Kickstart version ;-) rb
        if self.last_image is not None:
            outputs = self.model.predict(self.last_image[None, :, :, :])
            steering = outputs[0][0][0]
            throttle = outputs[1][0][0]

            #cv2.imshow("CarView", self.last_image)
            #cv2.waitKey(0)
            '''
            if self.mylastspeed <= self.myspeed:
                print("---")
            if self.mylastspeed > self.myspeed:
                print("+++")
            '''
            if self.myspeed < 14:
                throttle0 = throttle
                if abs(steering) < 0.4:
                    if throttle < 0.7:
                        throttle = 0.7
                        print("*** 0.7 ***", throttle0)

                if abs(steering) < 0.3:
                    if throttle < 0.85:
                        throttle = 0.85
                        print("*** 0.8 ***", throttle0)

                if abs(steering) < 0.2:
                    if throttle < 0.95:
                        throttle = 0.95
                        print("*** 0.9 ***", throttle0)

                if abs(steering) < 0.1:
                    if throttle < 1:
                        throttle = 1.0
                        print("*** 1.0 ***", throttle0)
            
            
            self.send_controls(steering, throttle)



def race(model_path, host, name):

    # race cockpit
    #cv2.namedWindow("CarView")

    # Load keras model
    model = keras.models.load_model(model_path)
    model.compile(optimizer='adam', loss='mse')
    model.summary()

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

    '''
    AI_LAUNCH_DURATION = 2.7 #3.0            # the ai will output throttle for this many seconds
    AI_LAUNCH_THROTTLE = 1.7 #1.8 
    '''
    maxcount = int(2.7/0.2) #2.7s 20Hz
    print("maxcount: ", maxcount)
    AI_START = True
    try:
        if AI_START:
            for i in range(maxcount): 
                client.send_controls(-0.05,1.)
                time.sleep(0.2)
                print("AI kick start", i)
            AI_START = False
            
        while True:
            client.update()
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    client.stop()

if __name__ == '__main__':
    args = docopt(__doc__)
    race(model_path = args['--model'], host = args['--host'], name = args['--name'])

'''
import cv2
import matplotlib.pyplot as plt

# Read single frame avi
cap = cv2.VideoCapture('singleFrame.avi')
rval, frame = cap.read()

# Attempt to display using cv2 (doesn't work)
cv2.namedWindow("Input")
cv2.imshow("Input", frame)

#Display image using matplotlib (Works)
b,g,r = cv2.split(frame)
frame_rgb = cv2.merge((r,g,b))
plt.imshow(frame_rgb)
cv2.imshow('image',img)
cv2.waitKey(0)
plt.title('Matplotlib') #Give this plot a title, 
                        #so I know it's from matplotlib and not cv2
plt.show()
'''