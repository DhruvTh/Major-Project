#importing required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scipy.ndimage
import matplotlib
import pickle

def animate(i):
    data=np.zeros((16,16))
    tick=True
    xy=[]
    while(tick):
        try:
            with open('C:/python 3.9/Scripts/data.pkl', 'rb') as file:
                data = pickle.load(file)
            tick=False
        except:
            pass
    data = scipy.ndimage.zoom(data,10, mode='nearest')
    
    # for i in range(0,1024):
    #     xy.append([i,np.argmax(data[i])])
    plt.cla()
    plt.axis('off')
    plt.pcolormesh(data, vmin=0, vmax=100, cmap='jet')# shading='gouraud')

ani = FuncAnimation(plt.figure(figsize=(10,10)), animate, interval=200)

plt.show()


