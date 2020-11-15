import xml.etree.ElementTree as ET
import glob
import numpy as np 
import csv
# annotation_file = f"Annotations/{image_id}.xml"
files =[]
with open('file.csv', 'w', newline='') as csvfile:
    csvfile = csv.writer(csvfile, delimiter=',',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
    for item in glob.glob("thor_data_label/*.xml"):
        files = np.append(item,files)
        annotation_file = files[0]
        tree = ET.parse(annotation_file)
        name = tree.find("filename").text
        print(name)
        row= [f'{name}']
        csvfile.writerow(row)
