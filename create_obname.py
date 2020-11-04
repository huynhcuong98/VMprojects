import cv2
import numpy as np
import csv
import glob
import os
from numpy.random import randint as rd
import xml.etree.cElementTree as ET
import shutil


fd_anno ='Labels_changed'
if os.path.exists(fd_anno):
        shutil.rmtree(fd_anno)

os.makedirs(fd_anno)

root_xml = 'labels'
root_img = 'images'

xmls = os.listdir(root_xml)
# img = os.listdir(root_img)

def read_xml(root, path):
    box =[]
    print(f'{root}/{path}')
    tree = ET.parse(f'{root}/{path}')

    root = tree.getroot()

    for member in root.findall('object'): 
        value = (int(member.find('bndbox')[0].text),
                 int(member.find('bndbox')[1].text),
                 int(member.find('bndbox')[2].text),
                 int(member.find('bndbox')[3].text)
                 )
        c = member.find('name').text
        box.append([c,value])
    return box
def main():
	clas5 = 'cam-rephai','cam-retrai', 'cam-xehoi', 'v-kdc', 'v-end-kdc'
	tocdo = 'cam-v40','cam-v50','cam-v60','cam-v70','cam-v80','cam-v90','cam-v100','cam-v120','cam-v5','cam-v10','cam-15','cam-v20','cam-v25','cam-v30'

	for xml in xmls:
		boxes = read_xml(root_xml, xml)
		path_img = f'{xml[:-4]}.jpg'
		img = cv2.imread(f'{root_img}/{path_img}')

		annotation = ET.Element('annotation')
		ET.SubElement(annotation, 'folder').text = 'Data'
		ET.SubElement(annotation, 'filename').text = f"{path_img}"
		source = ET.SubElement(annotation, 'source')
		ET.SubElement(source, 'database').text = 'Unknown'
		ET.SubElement(source, 'annotation').text = 'VOC'
		ET.SubElement(source, 'image').text = 'flickr'
		ET.SubElement(source, 'flickr').text = '-1'
		ET.SubElement(annotation, 'segmented').text = '0'
		size = ET.SubElement(annotation, 'size')
		ET.SubElement(size, 'width').text = str(img.shape[1])
		ET.SubElement(size, 'height').text = str(img.shape[0])
		ET.SubElement(size, 'depth').text = "3"


		############# ghi lai thong tin xml cu
		for box in boxes:
			x= box[1][0]
			y= box[1][1]
			x2=box[1][2]
			y2=box[1][3]

			name= str(box[0])
			if name in tocdo:
				name = 'cam-tocdo'
			elif name not in clas5:
				name = "unknown"

			ob = ET.SubElement(annotation, 'object')
			ET.SubElement(ob, 'name').text = name
			ET.SubElement(ob, 'pose').text = 'Unspecified'
			ET.SubElement(ob, 'truncated').text = '0'
			ET.SubElement(ob, 'difficult').text = '0'
			bbox = ET.SubElement(ob, 'bndbox')
			ET.SubElement(bbox, 'xmin').text = str(box[1][0])
			ET.SubElement(bbox, 'ymin').text = str(box[1][1])
			ET.SubElement(bbox, 'xmax').text = str(box[1][2])
			ET.SubElement(bbox, 'ymax').text = str(box[1][3])

		tree = ET.ElementTree(annotation)
		tree.write(f"Labels_changed/{xml}")
		# cv2.imwrite(f'Images/{xml[:-4]}.jpg', img)				

main()
