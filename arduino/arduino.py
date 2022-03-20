
from distutils.log import error
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import scipy.ndimage
import matplotlib
import serial
import serial.tools.list_ports
import json
from flask import Flask, request, render_template, Response, make_response
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import threading
import pandas as pd

matplotlib.use('agg')


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)


class Arduino:
    def __init__(self):        
        
        self.cap2 = False
        self.data = np.zeros([16,16])
        self.cop = 'off'
        self.est = '0'
        self.caph=[0,0]
        self.capst=0
        self.listimg=[]
        self.start=True
        self.vdiv=80
        self.hdiv1=53
        self.hdiv2=106
        self.divp=np.array([0,0,0,0,0,0,0])
        self.listexl=[]

    def arduino_est(self):
        try:
            ports = serial.tools.list_ports.comports()
            if(ports==[] or ports==None):
                self.est='0'
            for i in ports:
                st=str(i)
                if('usbmodem' in st):
                    port=i[0]
                if('COM' in st):
                    port=i[0]
                else:
                    self.est='0'
            self.serialport=serial.Serial(port,baudrate=115200)
            self.est='1'
        except:
            self.est='0'
    
    def arduino_read(self):
        tick=True
        while tick:
            if(self.est=='1'):
                try:
                    adata= self.serialport.readline()
                    data2=adata.decode('Ascii').rstrip().split(',')
                    data1=[int(i) for i in data2]
                    self.data[data1[0]][data1[1]]=data1[2]
                except:
                    # print('error:',adata)
                    ports = serial.tools.list_ports.comports()
                    if(ports==[] or ports==None):
                        self.est='0'

    def animate1(self):
        if(self.start==True):
            Arduino.arduino_est(self)
            self.start=False
            thread = threading.Thread(target=Arduino.arduino_read,args=(self,))
            thread.start()
        x,y=[],[]
        for i in range(0,16):
            for j in range(0,16):
                x.append(i)
                y.append(j)
        while self.est=='1':
            fig = plt.figure(figsize=(20,8))
            ax = fig.add_subplot(1,2,1)
            #self.data=np.random.randint(150,size=(16,16))
            data1 = scipy.ndimage.zoom(self.data,10, mode='nearest')
            ax.pcolormesh(data1, vmin=0, vmax=100, cmap='jet')
            ax.axis('off')
            z=list(self.data.flatten())
            mx,my,my1=[],[],[]            
            if(self.cop=='on'):
                for i in range(0,160):
                    mx.append(i)
                    my.append(np.argmax(data1[i,:self.vdiv]))
                    my1.append(np.argmax(data1[i,self.vdiv:]))
                mx=np.array(mx)
                my=np.array(my)
                my1=np.array(my1)
                ax.plot(my,mx)
                ax.plot(my1+self.vdiv,mx)
            bottom = np.zeros_like(z)
            width = depth = np.ones_like(z)
            ay = fig.add_subplot(1, 2, 2, projection='3d')
            ay.set_zlim(0, 200)
            ay.bar3d(x, y, bottom, width, depth, z,shade=True)
            fig.canvas.draw()
            img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
            img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            img1=img[50:750,205:1000,:]
            #img1 = cv2.copyMakeBorder(img1, 40, 40, 40, 20, cv2.BORDER_CONSTANT, None, value = 0)
            img2=img[100:750,1100:1800,:]
            #img2 = cv2.copyMakeBorder(img2, 40, 40, 20, 40, cv2.BORDER_CONSTANT, None, value = 0)
            img1=cv2.resize(img1,(500,450))
            img1=cv2.line(img1, pt1=(30+int(self.vdiv*440/160),30), pt2=(30+int(self.vdiv*440/160),425), color=(0,0,0), thickness=2)
            img1=cv2.line(img1, pt1=(30,30+int(self.hdiv1*395/160)), pt2=(470,30+int(self.hdiv1*395/160)), color=(0,0,0), thickness=2)
            img1=cv2.line(img1, pt1=(30,30+int(self.hdiv2*395/160)), pt2=(470,30+int(self.hdiv2*395/160)), color=(0,0,0), thickness=2)
            img2=cv2.resize(img2,(500,450))
            img=np.hstack((img1,img2))
            plt.close()
            div1=np.hsplit(data1,[self.vdiv])
            div1=[(sum(j[j!=0])/(len(j[j!=0]) or 1)) for i in div1 for j in np.vsplit(i,[self.hdiv1,self.hdiv2])]
            div1.append((sum(self.data[self.data!=0])/(len(self.data[self.data!=0]) or 1)))
            div1=np.array(div1)
            self.divp= np.round((0.000000388*(div1**5)- 0.000087126*(div1**4)+ 0.008421021*(div1**3)- 0.275899413*(div1**2) + (4.714242168*div1)),1)
            self.caph.append(int(self.cap2))
            self.caph.pop(0)
            if(self.caph[0]==1 and self.caph[1]==1):
                self.listimg.append(img)
                self.listexl.append(self.divp)
            if(self.caph[0]==1 and self.caph[1]==0):
                height, width, layers = img.shape
                size = (width,height)
                now = time.time()
                out = cv2.VideoWriter('saved_videos/'+str(now)+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 3, size)
                for i in range(len(self.listimg)):
                    out.write(np.uint8(self.listimg[i]))
                out.release()
                df = pd.DataFrame(self.listexl,columns=['Right Front','Right Mid','Right End','Left Front','Left Mid','Left End','Overall Average'])
                writer = pd.ExcelWriter('saved_videos/'+str(now)+'.xlsx')
                df.to_excel(writer, index=False)
                writer.save()
                self.listimg=[]
                self.listexl=[]            
            
            ret2, buffer2 = cv2.imencode('.jpg', img)
            frame = buffer2.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')   


com = [Arduino()]
capture = ['']


@app.route('/video')
def video():
    return Response(com[0].animate1(), mimetype='multipart/x-mixed-replace; boundary=frame')


cop = ['off']
connection = [''] 
ragTemp = ['','','']

@app.route('/', methods=['GET', 'POST'])
def arduino():
    
    if request.method == "POST":
        cop[0] = request.values.get('cop')
        capture[0] = request.values.get('cap1')
        connection[0] = request.values.get('connection')
        ragTemp[0] = request.values.get('rangeInput')
        ragTemp[1] = request.values.get('rangeInput1')
        ragTemp[2] = request.values.get('rangeInput2')

        
    if(cop[0] != '' and cop[0] != None):
        com[0].cop = cop[0]
    
    if(capture[0] != '' and capture[0] != None):
        com[0].cap2 = capture[0]


    if(connection[0] != '' and connection[0] != None):
        com[0].arduino_est()

    if(ragTemp[0] != '' and ragTemp[0] != None):
        com[0].vdiv = int(ragTemp[0])

    if(ragTemp[1] != '' and ragTemp[1] != None):
        com[0].hdiv1 = int(ragTemp[1])

    if(ragTemp[2] != '' and ragTemp[2] != None):
        com[0].hdiv2 = int(ragTemp[2])
    
    return render_template('arduino.html', cop = com[0].cop, cap1 = com[0].cap2, range = [com[0].vdiv,com[0].hdiv1,com[0].hdiv2])


@app.route('/avp')
def avp():
    data = com[0].divp
    data = data.tolist()
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/emsg')
def emsg():
    data = [com[0].est] 
    response = make_response(json.dumps(data[0]))
    response.content_type = 'application/json'
    return response
    

if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)
    
    