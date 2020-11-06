import cv2
import numpy as np
import csv
import glob
import os
from numpy.random import randint as rd
import xml.etree.cElementTree as ET
import shutil
from imgaug import augmenters as iaa


fd_anno ='Annotations'
fd_img = 'Images'

if os.path.exists(fd_anno):
        shutil.rmtree(fd_anno)
os.makedirs(fd_anno)

# if os.path.exists(fd_img):
#         shutil.rmtree(fd_img)
# os.makedirs(fd_img)

def xml_to_csv(root, path):
    # print(f'{root}/{path}')
    tree = ET.parse(f'{root}/{path}')
    root = tree.getroot()
    obs = []
    for member in root.findall('size'):
        width = member.find('width').text
        height = member.find('height').text

    for member in root.findall('object'): 
        value = (member.find('name').text,
                 int(member.find('bndbox')[0].text),
                 int(member.find('bndbox')[1].text),
                 int(member.find('bndbox')[2].text),
                 int(member.find('bndbox')[3].text)
                 )
        c = str(value[0])
        bndbox = value[1], value[2], value[3], value[4]
        ob = [c, bndbox]
        obs.append(ob)
    return width,height, obs
def process(name,width,height, obs):

	annotation = ET.Element('annotation')
	ET.SubElement(annotation, 'folder').text = 'Data'
	ET.SubElement(annotation, 'filename').text = f"{name[:-4]}.jpg"
	source = ET.SubElement(annotation, 'source')
	ET.SubElement(source, 'database').text = 'Unknown'
	ET.SubElement(source, 'annotation').text = 'VOC'
	ET.SubElement(source, 'image').text = 'flickr'
	ET.SubElement(source, 'flickr').text = '-1'
	ET.SubElement(annotation, 'segmented').text = '0'
	size = ET.SubElement(annotation, 'size')
	ET.SubElement(size, 'width').text = f'{width}'
	ET.SubElement(size, 'height').text = f'{height}'
	ET.SubElement(size, 'depth').text = "3"

	#Get value for each ob 
	for i in range(len(obs)):
		dir_ob1= obs[i]  
		# print(dir_ob1)
		ob_name = dir_ob1[0]
		box = dir_ob1[1]

		ob = ET.SubElement(annotation, 'object')
		ET.SubElement(ob, 'name').text = ob_name
		ET.SubElement(ob, 'pose').text = 'Unspecified'
		ET.SubElement(ob, 'truncated').text = '0'
		ET.SubElement(ob, 'difficult').text = '0'
		bbox = ET.SubElement(ob, 'bndbox')
		ET.SubElement(bbox, 'xmin').text = str(box[0])
		ET.SubElement(bbox, 'ymin').text = str(box[1])
		ET.SubElement(bbox, 'xmax').text = str(box[2])
		ET.SubElement(bbox, 'ymax').text = str(box[3])
	# print(name)
	tree = ET.ElementTree(annotation)
	tree.write(f"Annotations/{name}")
	# cv2.imwrite(f'Images/{path_img}',img )				

class fill(object):
	def __init__(self,root_roi):
		self.root_roi = root_roi

		self.rois= os.listdir(self.root_roi)

	def main(self):
		# print(self.root_roi)
		for roi in self.rois:
			width,height, obs = xml_to_csv(self.root_roi, roi)
			process(roi,width,height, obs)
	

a = fill(root_roi = 'test_labels')
a.main()
