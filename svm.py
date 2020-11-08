import os
import numpy as np 
import joblib
from skimage.feature import hog
import cv2


cam_rephai = joblib.load('model/cam-rephai.xml')
cam_retrai = joblib.load('model/cam-retrai.xml')
cam_xehoi = joblib.load('model/cam-xehoi.xml')
v_kdc = joblib.load('model/v-kdc.xml')
v_end_kdc = joblib.load('model/v-end-kdc.xml')

class apply_svm(object):
  def __init__(self,cam_rephai,cam_retrai, cam_xehoi, v_kdc, v_end_kdc):
    self.cam_rephai = cam_rephai, 'cam-rephai'
    self.cam_retrai = cam_retrai, 'cam-retrai'
    self.cam_xehoi = cam_xehoi, 'cam-xehoi'
    self.v_kdc = v_kdc, 'v-kdc'
    self.v_end_kdc = v_end_kdc, 'v-end-kdc'
    self.l_model = self.cam_rephai, self.cam_retrai, self.cam_xehoi
                self.v_kdc, self.v_end_kdc
  def svm_classify(sefl, x,img1, c):
    roi = img1[int(x[1]):int(x[3]),int(x[0]):int(x[2])]
    img = cv2.resize(roi, (40,40))
    fd, hog_image = hog(img, orientations = 9, pixels_per_cell= (5,5), cells_per_block = (8,8), visualize = True, multichannel = True)
    fd=fd.reshape(1,-1)

    for model in self.l_model:
      if c == model[1]:
        self.clf= self.model[0]

    pre = self.clf.predict(fd)
    return pre[0] 