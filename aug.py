import cv2
import numpy as np
import csv
import glob
import os
from numpy.random import randint as rd
import xml.etree.cElementTree as ET
import shutil
from imgaug import augmenters as iaa


fd_anno ='Annotations_aug'
fd_img = 'Images'

if os.path.exists(fd_anno):
        shutil.rmtree(fd_anno)
os.makedirs(fd_anno)

if os.path.exists(fd_img):
        shutil.rmtree(fd_img)
os.makedirs(fd_img)

l_folder = 'cam-retrai', 'cam-rephai', 'cam-xehoi', 'v-kdc', 'v-end-kdc', 'cam-tocdo'

# l_folder = 'cam-retrai', 'cam-rephai'
def hstack(bg, roi):
	try:
		x = np.random.randint(int(0.1*bg.shape[1]),bg.shape[1]-roi.shape[1]-int(0.1*bg.shape[1]))
		y = np.random.randint(int(0.2*bg.shape[0]),bg.shape[0]-roi.shape[0]-int(0.4*bg.shape[0]))
	except:
		roi = cv2.resize(roi, (int(roi.shape[0]*0.5), int(roi.shape[1]*0.5)))
		x = np.random.randint(int(0.1*bg.shape[1]),bg.shape[1]-roi.shape[1]-int(0.1*bg.shape[1]))
		y = np.random.randint(int(0.2*bg.shape[0]),bg.shape[0]-roi.shape[0]-int(0.4*bg.shape[0]))

	bg[y:y+roi.shape[0], x:x+roi.shape[1]] = roi

	return int(x), int(y), int(x+roi.shape[1]), int(y+roi.shape[0])


def process(roi,path_img, img, ob_name):
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

	#Get value for each ob 

	dir_ob1= hstack(img, roi)   
	ob = ET.SubElement(annotation, 'object')
	ET.SubElement(ob, 'name').text = ob_name
	ET.SubElement(ob, 'pose').text = 'Unspecified'
	ET.SubElement(ob, 'truncated').text = '0'
	ET.SubElement(ob, 'difficult').text = '0'
	bbox = ET.SubElement(ob, 'bndbox')
	ET.SubElement(bbox, 'xmin').text = str(dir_ob1[0])
	ET.SubElement(bbox, 'ymin').text = str(dir_ob1[1])
	ET.SubElement(bbox, 'xmax').text = str(dir_ob1[2])
	ET.SubElement(bbox, 'ymax').text = str(dir_ob1[3])

	tree = ET.ElementTree(annotation)
	tree.write(f"Annotations_aug/{path_img[:-4]}.xml")
	cv2.imwrite(f'Images/{path_img}',img )				

class fill(object):
	def __init__(self,idx, root_img, root_roi, ob_name):
		self.idx =idx 
		self.root_roi = root_roi
		self.root_img = root_img
		self.ob_name = ob_name

		self.imgs= os.listdir(self.root_img)
		self.rois= os.listdir(self.root_roi)

	def main(self):
		j = 0
		print(self.root_roi)
		print(f'fill {5001 - len(self.rois)} images')

		for i in range(self.idx, self.idx + 5001 - len(self.rois)):
			path_img = self.imgs[i]
			if j < len(self.rois):
				path_roi = self.rois[j]
			else:
				path_roi = self.rois[rd(len(self.rois))]
			img = cv2.imread(f'{self.root_img}/{path_img}')
			img = cv2.resize(img,(960,540))
			roi = cv2.imread(f'{self.root_roi}/{path_roi}')
			j+=1
			seq = iaa.Sequential([iaa.AdditiveGaussianNoise(loc=0, scale=(10, 20), per_channel=True)])
			roi = seq(image=roi)
			process(roi,path_img,img, self.ob_name)
		return i,j 	
i=0
for folder in l_folder:
	a = fill(idx = i ,root_img = 'none',root_roi = f'rois/{folder}', ob_name = folder)
	i,j= a.main()
	print(f'filled {folder}: {j} images ')
