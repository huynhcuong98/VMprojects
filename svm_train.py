    
import glob
import time
import cv2
from collections import deque
import numpy as np
import pandas as pd
from skimage.feature import hog
from sklearn import svm
import joblib

def train_SVC(X_train, y_train):
    """
        Function to train an svm.
    """
    svc = svm.LinearSVC( C=0.005,max_iter=10000)
    # svc=svm.SVC(kernel = "rbf" , gamma = 10, coef0 = 0)
    # Check the training time for the SVC
    t=time.time()
    print("1")
    svc.fit(X_train, y_train)
    t2 = time.time()
    print(round(t2-t, 2), 'Seconds to train SVC...')
    return svc
class train_ob(object):
    def __init__(self, pos, neg, n_sample):
        self.pos = pos
        self.neg = neg 
        self.n_sample = n_sample
        self.folder = self.pos, self.neg
        print(self.folder)
    def setup_train_data(self):
        X_train = []
        y_train = []

        for i in range(len(self.folder)):
            listitem=[]
            for item in glob.glob(f'data/{self.folder[i]}/*.jpg'):
                listitem.append(item)
            print(f"{self.folder[i]}:"+str(len(listitem)))
            for j in range(self.n_sample):
                img = cv2.imread("{}".format(listitem[j]))           #40x40x3
                # dim = np.random.randint(15,24)
                dim = 40
                dims=(dim,dim)
                img = cv2.resize(img, dims)
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                fd, hog_image = hog(img, orientations = 9, pixels_per_cell= (5,5), cells_per_block = (8,8), visualize = True, multichannel = True)
                # print(len(fd))
                y_train = np.append(y_train,f"{self.folder[i]}")
                X_train = np.append(X_train,fd)  
        # print(len(listitem))
        return X_train, y_train
    print('Preparing training data...')
    def main(self):
        X_train, y_train = self.setup_train_data()
        X_train= X_train.reshape(-1,576).astype('float32')
        print(X_train.shape) # shape = (6000,576)
        print(y_train.shape) #shape = (6000,1)
        svc = train_SVC(X_train, y_train)
        filename = f'model/{self.pos}.xml'
        joblib.dump(svc, filename, protocol= 2)

def crp():
    cam_rephai = train_ob(pos = 'cam-rephai', neg=  'noise1',n_sample=1220)
    cam_rephai.main()
def crt():
    cam_retrai = train_ob(pos = 'cam-retrai', neg=  'noise1',n_sample=1400)
    cam_retrai.main()
def cxh():
    cam_xehoi = train_ob(pos = 'cam-xehoi', neg=  'noise1',n_sample=1200)
    cam_xehoi.main()
def vkdc():
    vkdc = train_ob(pos = 'v-kdc', neg=  'noise1',n_sample=1800)
    vkdc.main() 
def vekdc():
    vekdc = train_ob(pos = 'v-end-kdc', neg=  'noise1',n_sample=1800)
    vekdc.main() 
def ctd():
    cam_tocdo = train_ob(pos = 'cam-tocdo', neg=  'noise_camtocdo',n_sample=3000)
    cam_tocdo.main() 
def main():
    # crp()
    # crt()
    # cxh()
    # vkdc()
    # vekdc()
    ctd()
main()