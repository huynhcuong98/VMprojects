import xml.etree.ElementTree as ET
import glob
import numpy as np 
import csv
import os

root = 'train_labels'
files = os.listdir(root)
def get_index(n):
    index = ['0','0','0','0','0','0','0','0']
    n = str(n)
    for i in range(len(n)):
        index.pop(0)
        index.append(n[i])
    print('index', index)
    s=''
    for it in index:
        s += str(it)
    return s
# for it in f:
#     print(it)
#     os.rename(f'{root}/{it}', f'{root}/{it}.jpg')
for i in range(len(files)):
    new_name = get_index(i)
    os.rename(f'train_images/{files[i][:-4]}.jpg', f'train_images/{new_name}.jpg')
    os.rename(f'train_labels/{files[i]}', f'train_labels/{new_name}.xml')
