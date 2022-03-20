
from multiprocessing import process
from operator import pos
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from datetime import datetime
import time
import matplotlib
import pandas as pd
import json

from flask import Flask, escape, request, render_template, Response, make_response, redirect
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2

matplotlib.use('agg')


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)



class pose_estimation:
    def __init__(self, processing = 'low'):
        if (processing=='low'):
            self.model='mobilenet_thin'
            self.resize='432x368'
        if (processing=='high'):
            self.model='cmu'
            self.resize='656x368'
            
        
        self.w, self.h = model_wh(self.resize)
        self.e = TfPoseEstimator(get_graph_path(self.model), target_size=(self.w, self.h))
        
        self.rangle = 0
        self.langle = 0
        self.cap1 = 0
        self.swing = 0
        self.caph=[0,0]
        self.capst=0
        self.listimg=[]
        self.listexl=[]
        
    def pose1(self):
        self.vid = cv2.VideoCapture(0)
        while True:
            ret, frame = self.vid.read()
            #if(ret == True):
            frame = cv2.flip(frame,1)

            humans = self.e.inference(frame, resize_to_default=(self.w > 0 and self.h > 0), upsample_size=4.0)
            human_with_ske = TfPoseEstimator.draw_humans(frame, humans, imgcopy=False)    
            black_background = np.zeros(frame.shape)
            skeleton = TfPoseEstimator.draw_humans(black_background, humans, imgcopy=False)
                
            if(humans==[]):
                humans='No'

            partlist=[]
            stri=str(humans[0])
            partlist=[]
            for i in range(0,18):
                le='BodyPart:'+str(i)+'-('
                if(le in stri):
                    start=stri.index('BodyPart:'+str(i)+'-')+len(le)
                    in1=float(stri[start:start+4])
                    in2=float(stri[start+6:start+10])
                    partlist.append([True,in1,in2])
                else:
                    partlist.append([False,0,0])
            partlist=np.array(partlist)           
            if(partlist[8][0]==True and partlist[9][0]==True and partlist[10][0]==True):
                l1=partlist[9][1:]-partlist[10][1:]
                l2=partlist[9][1:]-partlist[8][1:]
                arg = sum(l1*l2)/(np.linalg.norm(l1)*np.linalg.norm(l2))
                self.rangle=round(np.arccos(arg)*180/np.pi, 1)
                skeleton= cv2.putText(skeleton, "Right angle:"+str(self.rangle),(50,50) , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0, cv2.LINE_AA)
            
            if(partlist[11][0]==True and partlist[12][0]==True and partlist[13][0]==True):
                l1=partlist[12][1:]-partlist[13][1:]
                l2=partlist[12][1:]-partlist[11][1:]
                arg = sum(l1*l2)/(np.linalg.norm(l1)*np.linalg.norm(l2))
                self.langle=round(np.arccos(arg)*180/np.pi, 1)
                skeleton = cv2.putText(skeleton, "Left angle:"+str(self.langle), (50,90) , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0, cv2.LINE_AA)

            if(partlist[1][0]==True and partlist[8][0]==True and partlist[11][0]==True):
                spoint=(partlist[8][1:]+partlist[11][1:])/2
                l1=spoint-partlist[1][1:]
                l2=np.array([0,1])
                arg = sum(l1*l2)/(np.linalg.norm(l1)*np.linalg.norm(l2))
                self.swing=round(np.arccos(arg)*180/np.pi, 1)
                skeleton = cv2.putText(skeleton, "Swing angle:"+str(self.swing), (50,130) , cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 0, cv2.LINE_AA)
                    
                
            human_with_ske = cv2.copyMakeBorder(human_with_ske, 40, 40, 40, 20, cv2.BORDER_CONSTANT, None, value = 0)
            skeleton = cv2.copyMakeBorder(skeleton, 40, 40, 20, 40, cv2.BORDER_CONSTANT, None, value = 0)
            human_with_ske=cv2.resize(human_with_ske,(600,550))
            skeleton=cv2.resize(skeleton,(600,550))
            img=np.hstack((human_with_ske,skeleton))

            #cv2.imshow('img', img)
            #cv2.imwrite('img.jpg',img)
                
            self.caph.append(int(self.cap1))
            self.caph.pop(0)
                    
            if(self.caph[0]==1 and self.caph[1]==1):
                self.listimg.append(img)
                self.listexl.append([self.rangle,self.langle,self.swing])
            if(self.caph[0]==1 and self.caph[1]==0):
                height, width, layers = img.shape
                size = (width,height)
                now = time.time()
                out = cv2.VideoWriter('saved_videos/'+str(now)+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 2, size)
                for i in range(len(self.listimg)):
                    out.write(np.uint8(self.listimg[i]))
                out.release()
                df = pd.DataFrame(self.listexl,columns=['Right Angle','Left Angle','Swing Angle'])
                writer = pd.ExcelWriter('saved_videos/'+str(now)+'.xlsx')
                df.to_excel(writer, index=False)
                writer.save()
                self.listimg=[]
                self.listexl=[]
                    
            ret2, buffer2 = cv2.imencode('.jpg', img)
            frame = buffer2.tobytes()

            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # else:
            #     self.vid.release()
            #     cv2.destroyAllWindows()
            #     self.vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            

com = [pose_estimation()]
processing = ['low']
capture = ['']


@app.route('/', methods=['GET', 'POST'])
def index():
        
    if request.method == "POST":
        processing[0] = request.values.get('processing')
        capture[0] = request.values.get('cap1')
        
    if(capture[0] != '' and capture[0] != None):
        com[0].cap1 =  capture[0]
    
    if(processing[0] != '' and processing[0] != None ):
        com[0] = pose_estimation(processing[0])
        
    return render_template('index.html', processing = processing[0], cap1 = capture[0])
            
    
@app.route('/video1')
def video1():
    return Response(com[0].pose1(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/data')
def data():
    data = [com[0].langle, com[0].rangle, com[0].swing]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response



if __name__ == '__main__':
    app.debug = False
    app.run()
    
    