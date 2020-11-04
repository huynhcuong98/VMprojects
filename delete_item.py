import os

# 1 : chua file chuan
# 2 : chua file thua
root_1 = 'labels'
root_2 = 'images'

fd1 = os.listdir(root_1)
fd2 = os.listdir(root_2)

name = [it[:-4] for it in fd1]
dem =0
for it in fd2:
    if it[:-4] not in name:
        print(it)
        os.remove(f'{root_2}/{it}')
        dem+=1
print(dem)
