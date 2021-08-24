import bluetooth

from pynput.keyboard import Key,Controller

import cv2
import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
import subprocess

import time
import string






cam = False
micAndSpeak = False
wifi = False
blue = False

keyboard = Controller()



#Camera

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if cap is None or not cap.isOpened():
    print('Broken or no camera.')
    print('Detected: ',cap)
else:
    print('Taking picture.')
    videoCaptureObject = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    result = True
    while(result):
        ret,frame = videoCaptureObject.read()
        cv2.imwrite('testPicture.jpg',frame)
        result = False
    videoCaptureObject.release()
    cv2.destroyAllWindows()
    print('Picture taken, saved as testPicture.jpg')
    cam = True

    



#Mic + Sound



for i in range(50):
    keyboard.press(Key.media_volume_up)
    keyboard.release(Key.media_volume_up)
    i += 1
    time.sleep(0.01)



#print(sd.default.device)

if sd.default.device != '[]':
    print('Recording audio for 5 seconds.')
    fs = 44100  # Sample rate
    seconds = 5

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  
    write('output.wav', fs, myrecording)  
    print('Playing audio')
    playsound('output.wav')

    micAndSpeak = True
else:
    print('Broken or no mic.')
    
for x in range(50):
    keyboard.press(Key.media_volume_down)
    keyboard.release(Key.media_volume_down)
    x += 1
    time.sleep(0.01)




#bluetooth
print('Testing bluetooth.')
nearby_devices = bluetooth.discover_devices()
#print(nearby_devices)
if str(nearby_devices) != '[]':
    print('Bluetooth devices nearby: ',nearby_devices)
    blue = True

print(' ')
print(' ')

if cam:
    print('Camera - Check testPicture.jpg for pic')
else:
    print('Camera - Broken or no camera detected')
if micAndSpeak:
    print('Mic and Speaker - Did you hear it?')
else:
    print('Mic and Speaker - No mic detected and/or speakers didnt work')
if blue:
    print('Bluetooth - Bluetooth is working')
else:
    print('Bluetooth - none or broken bluetooth')
print(' ')
print(' ')

subprocess.call([r'intBatReport.bat'])

time.sleep(2)
print('Testing Battery')
file = open('battery-report.html','r')
inside = file.readlines()
report = str(inside)

start_index = report.find('DESIGN CAPACITY</span></td><td>')
end_index = start_index + 37
desCap = str(report[start_index + 31:end_index])

sec_start = report.find('FULL CHARGE CAPACITY</span></td><td>')
sec_end = sec_start + 42
fullCap = str(report[sec_start + 36:sec_end])


cyc_start = report.find('CYCLE COUNT</span></td><td>')
cyc_end = cyc_start + 32
#5
cycTotal = str(report[cyc_start + 27:cyc_end])



desEnd = ''.join(filter(str.isdigit, desCap))
fullEnd = ''.join(filter(str.isdigit, fullCap))





print('Design Capacity: ',desCap)
print('Full Charge Capacity: ',fullCap)
print('Design % = ',((int(fullEnd)/int(desEnd))*100))
print('Cycle Count: ',cycTotal)





