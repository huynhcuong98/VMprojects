import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import cv2

root = 'labels'
# files = os.listdir(root)
# print(f'path: {root}/{files[1]}')
files = [it for it in glob.glob('labels/*.xml')]
dem =0
def xml_to_csv(root, path):
    # print(f'{root}/{path}')
    # tree = ET.parse(f'{root}/{path}')
    tree = ET.parse(path)
    root = tree.getroot()
    i = 0
    ob = root.find('object')
    if ob == None:
        print(path)
        os.remove(path)
def main():
    for file in files:
        xml_to_csv(root,file)
main()
