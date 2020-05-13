from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import os
import datetime

channels = [12, 16, 20, 21, 13]
output_channel = 6



path = "Output/"

camera_on = True
video_on = False
ir_on = False

pushdown = datetime.datetime.now()

camera = PiCamera()
camera.framerate = 20
camera.start_preview()


GPIO.setmode(GPIO.BCM)
GPIO.setup(channels[0], GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(channels[1], GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(channels[2], GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(channels[3], GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(channels[4], GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(output_channel, GPIO.OUT)



def camera_on_off(a):
    global camera_on
    global pushdown
    pushdown = datetime.datetime.now()
    
    if camera_on:
        camera.stop_preview()
        camera_on = False
        print("Camera off")
    elif not camera_on:
        camera.start_preview()
        camera_on = True
        print("Camera on")
        

def capture_picture(a):
    path
    camera_was_on = camera_on
    global camera
    
    if not os.path.exists(path):
        os.makedirs(path)
        print("path made")
    
    if camera_on:
        camera.stop_preview
        
    camera_width = camera.resolution.width
    camera_height = camera.resolution.height
    camera.resolution = (3280, 2464)
    capture_path = path + datetime_string() + ".jpg"
    
    camera.capture(capture_path)
    
    camera.resolution = (camera_width, camera_height)
    print("picture captured")
    
    if camera_was_on:
        camera.start_preview()

def capture_video(a):
    global video_on
    global camera
    
    if not os.path.exists(path):
        os.makedirs(path)
        print("path made")
    
    if video_on:
        camera.stop_recording()
        video_on = False
        print("Recording stopped")
        
    elif not video_on:
        capture_path = path + datetime_string() + ".h264"
        camera.start_recording(capture_path)
        video_on = True
        print("Recording started")

def toggleIR(a):
    global ir_on
    
    if ir_on:
        GPIO.output(output_channel, GPIO.LOW)
        ir_on = False
        print("IR off")
    
    elif not ir_on:
        GPIO.output(output_channel, GPIO.HIGH)
        ir_on = True
        print("IR on")
    release = datetime.datetime.now()
    delta = release - pushdown
    seconds = delta.total_seconds()
    
    if (seconds < 1):
        powerDown(seconds)  
    
def powerDown(a):
    global camera
    print("Shutdown")
    
    #release = datetime.datetime.now()
    #delta = release - pushdown
    #seconds = delta.total_seconds()
        
    if video_on:
        camera.stop_recording()
    if camera_on:
        camera.stop_preview()
    if ir_on:
        GPIO.output(output_channel, GPIO.LOW)
        GPIO.cleanup()
        
    os.system("sudo poweroff -n")
    
def datetime_string():
    time = datetime.datetime.now()
    string = ""
    string += str(time.year) + "_"
    string += str(time.month) + "_"
    string += str(time.day) + " "
    string += str(time.hour) + "_"
    string += str(time.minute) + "_"
    string += str(time.second)
    return string

GPIO.add_event_detect(channels[0], GPIO.FALLING, callback=camera_on_off)
GPIO.add_event_detect(channels[1], GPIO.FALLING, callback=capture_picture)
GPIO.add_event_detect(channels[2], GPIO.FALLING, callback=capture_video)
GPIO.add_event_detect(channels[3], GPIO.FALLING, callback=toggleIR)
GPIO.add_event_detect(channels[4], GPIO.FALLING, callback=powerDown)


try:
    while True:
        #print("hi")
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Bye")




#camera.resolution = (2592, 1944)
#camera.start_preview()
#sleep(5)
#camera.stop_preview()


