import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import cv2

root = 'Annotations_aug'
files = os.listdir(root)
print(f'path: {root}/{files[1]}')
cam_re, cam_tocdo, kdc, unknown = 0, 0, 0, 0
n_clas = []
def xml_to_csv(root, path):
    print(f'{root}/{path}')
    tree = ET.parse(f'{root}/{path}')

    root = tree.getroot()
    i = 0
    for member in root.findall('object'): 
        value = (root.find('filename').text,
                 member.find('name').text,
                 i,
                 int(member.find('bndbox')[0].text),
                 int(member.find('bndbox')[1].text),
                 int(member.find('bndbox')[2].text),
                 int(member.find('bndbox')[3].text)
                 )
        name = value[0]
        c = value[1]
        idx = value[2]
        x,y,w,h = value[3], value[4], value[5], value[6]
        i+= 1
        # print(value)
        # img = cv2.imread(f'train_images/{name}')
        # roi = img[y:h,x:w]
        if c not in n_clas:
            n_clas.append(c)
        # if c not in ['cam-re', 'cam-tocdo', 'kdc', ] or c != 'kdc':
        #     c = 'unknown'
        # cv2.imwrite(f'rois/{c}/{name[:-4]}-{c}-{idx}.jpg', roi)
def main():
    for file in files:
        xml_to_csv(root,file)
    print(len(n_clas))
    print('n_clas:', n_clas)
main()
