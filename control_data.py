import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import cv2
import numpy as np 

root_xml = 'Labels1'

xml = os.listdir(root_xml)

columns = ['name']
def no_class(root, path):
    # print(f'{root}/{path}')
    tree = ET.parse(f'{root}/{path}')
    root = tree.getroot()
    for member in root.findall('object'): 
        value = (root.find('filename').text,
                 member.find('name').text,
                 int(member.find('bndbox')[0].text),
                 int(member.find('bndbox')[1].text),
                 int(member.find('bndbox')[2].text),
                 int(member.find('bndbox')[3].text)
                 )
        name = value[0]
        c = value[1]
        if c not in columns:
            columns.append(c)

for file in xml:
    no_class(root_xml,file)

# print('n_clas:', columns)
# print('total:', len(columns))
def initial_row(col,root, path):
    print(f'{root}/{path}')
    tree = ET.parse(f'{root}/{path}')

    root = tree.getroot()
    i = 0

    new_row= ['name']
    for i in range(len(col)-1):
        new_row.append(0)
    new_row[0] =  root.find('filename').text 
     
    for member in root.findall('object'): 
        c = member.find('name').text

        for i in range(len(col)):
            if c == col[i]:
                new_row[i] +=1 

    return new_row

def write_row(rows,col,root, path):
    print(f'{root}/{path}')
    tree = ET.parse(f'{root}/{path}')

    root = tree.getroot()
    i = 0
    new_row= ['name']
    for i in range(len(col)-1):
        new_row.append(0)
    new_row[0] =  root.find('filename').text 
     
    for member in root.findall('object'): 
        c = member.find('name').text

        for i in range(len(col)):
            if c == col[i]:
                new_row[i] +=1 
                
    # print('new_row:', new_row)
    # print('ROWS:',rows)
    for it in new_row:
    	rows.append(it)

rows= initial_row(columns, root_xml, xml[0])

for i in range(1,len(xml)):
	write_row(rows,columns, root_xml, xml[i])
	
rows = np.reshape(rows,(-1,len(columns)))
df = pd.DataFrame(data=rows, index=None, columns=columns, dtype=None)
df.to_csv(f'control_Labels1.csv', columns = None, index = None, sep =',')
