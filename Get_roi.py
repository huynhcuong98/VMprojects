import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import cv2

root = 'Annotations'
root_img = 'Images'
files = os.listdir(root)
print(f'path: {root}/{files[1]}')
n_clas = []

fd_rois ='rois'
if os.path.exists(fd_rois):
        shutil.rmtree(fd_rois)
os.makedirs(fd_rois)
fds = 'rois/cam-retrai', 'rois/cam-rephai', 'rois/cam-tocdo', 'rois/cam-xehoi', 'rois/v-kdc', 'rois/v-end-kdc', 'rois/unknown' ,'rois/negative'
for fd in fds:
    if os.path.exists(fd):
        shutil.rmtree(fd)
    os.makedirs(fd)

def xml_to_csv(root, path):
    # print(f'{root}/{path}')
    tree = ET.parse(f'{root}/{path}')
    root = tree.getroot()

    name = root.find('filename').text
    #print(name)
    img = cv2.imread(f'{root_img}/{name}')

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
        c = str(value[1])
        idx = value[2]
        x,y,w,h = value[3], value[4], value[5], value[6]
        i+= 1
        # print(value)
        roi = img[y:h,x:w]
        if c not in n_clas:
            n_clas.append(c)
        # print(f'roi/{name[:-4]}-{c}-{idx}.jpg')
        cv2.imwrite(f'rois/{c}/{name[:-4]}-{c}-{idx}.jpg', roi)
def main():
    for file in files:
        xml_to_csv(root,file)
    # xml_to_csv(root,file)
    # cv2.imshow('a',roi)
    # cv2.waitKey(0)
    print('n_clas:', n_clas)
main()
