import os
import time
import random
import subprocess

num_clients = 1 #4
#model_file = "lane_keeper.h5" 
#model_file = "parkinglotnerds5.h5" 
#model_file = "parkinglotnerds8.h5" 
model_file = "parkinglotnerds9_crop47.h5" 


body_styles = ["donkey", "bare", "car01"]
host = '127.0.0.1'
#sim_path = "/home/rainer/dev/37-donkey3/DonkeySimLinux/donkey_sim.x86_64"
procs = []

for i in range(num_clients):
    conf_file = "client%d.py" % i
    with open(conf_file, "wt") as outfile:
        outfile.write('WEB_CONTROL_PORT = 888%d\n' % i)
        outfile.write('WEB_INIT_MODE = "local"\n')
        outfile.write('DONKEY_GYM = True\n')
        outfile.write('DONKEY_SIM_PATH = "remote"\n')
        #outfile.write('DONKEY_SIM_PATH = "/home/rainer/dev/37-donkey3/DonkeySimLinux/donkey_sim.x86_64"\n')
        outfile.write('SIM_HOST = "%s"\n' % host)
        
        ###
        outfile.write('AI_THROTTLE_MULT = 1.1\n') 
        outfile.write('AI_LAUNCH_DURATION = 3.0\n')
        outfile.write('AI_LAUNCH_THROTTLE = 1.8\n')
        outfile.write('AI_LAUNCH_ENABLE_BUTTON = "R2"\n')
        outfile.write('AI_LAUNCH_KEEP_ENABLED = True\n')


        outfile.write('ROI_CROP_TOP = 47\n')
        ###

        iStyle = random.randint(0, len(body_styles) - 1)
        #body_style = body_styles[iStyle]
        body_style = "bare"
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        #outfile.write('GYM_CONF = { "body_style" : "%s", "body_rgb" : (%d, %d, %d), "car_name" : "ai%d", "font_size" : 100}\n' % (body_style, r, g, b, i+1))
        outfile.write('GYM_CONF = { "body_style" : "%s", "body_rgb" : (%d, %d, %d), "car_name" : "%s", "font_size" : 50}\n' % (body_style, r, g, b, model_file))
        outfile.close()

    #conf_file = "myconfig.py"
    command = "python manage.py drive --model=models/%s --myconfig=%s" % (model_file, conf_file)
    com_list = command.split(" ")
    print(com_list)
    proc = subprocess.Popen(com_list)
    procs.append(proc)
    time.sleep(1)


print("running for 5 min...")
try:
    time.sleep(60 * 5)
except:
    pass

print("stopping ai")
for proc in procs:
    proc.kill()
print('done')