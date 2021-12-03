from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from datetime import datetime
import hou
import matplotlib.pyplot as plt
import numpy as np
import cv2, os

# def inputNumber(message):
#       while True:
#               try:
#                       userInput = int(input(message))
#               except ValueError:
#                       print("Not an integer! Please type an int.")
#                       continue
#               else:
#                       return userInput
#                       break

while True:
        print("\n" * 40)
        print("Cleared Shell")
        fullpath = ""
        folder = hou.ui.readInput("Enter the folder path of Image, ending in \\", buttons= ("OK", "Cancel"))
        print("You\'ve set the folder path to: " + folder[1])
        if not folder[0] == 0:
                        break
        img_name = hou.ui.readInput("Enter name of Image:", buttons=("OK", "Cancel"))
        print("The image you would like to use is: " + img_name[1])
        os.chdir(str(folder[1] + str("\\")))
        print("The current working directory is: " + os.getcwd())
        fullpath = os.path.join(str(folder[1]), str(img_name[1]))
        print("The full path to the image is: " + fullpath)
        #break
        if not img_name[0] == 0:
                        break
        elif not os.path.isfile(img_name[1]):
                        print('File name doesn\'t exist or has no extention, please try again.\n')
        else:
                        k = hou.ui.readInput("How many masks:", buttons=("OK", "Cancel"))
                        print("Generating " + str(k[1]) + " masks.")
                        #k = inputNumber('How many masks: ')
                        b = hou.ui.readInput("Blur strength:", buttons=("OK", "Cancel"))
                        print("Using a blur strength of " + b[1])
                        #b = inputNumber('Blur strength: ')
        break

# create folder

dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime('%d%m%y %H.%M.%S')
path = timestampStr
os.makedirs(path)
print("Generating folder " + timestampStr + " now.")
                                
# read
img = cv2.imread(img_name[1])
image_2d = img.reshape((img.shape[0] * img.shape[1], 3))
#cv2.imshow(img_name, fullpath)

# supplying the number of clusters we wish to generate
# kmeans_cluster = KMeans(n_clusters=k) # this is slower but more accurate
kmeans_cluster = MiniBatchKMeans(n_clusters=k[1]) 
kmeans_cluster.fit(image_2d) # clusters our list of pixels

cluster_centers = kmeans_cluster.cluster_centers_ # dominant colors array
cluster_labels = kmeans_cluster.labels_

result = cluster_centers[cluster_labels]
result = np.reshape(result, (img.shape))
cv2.imwrite(f'{path}/colormap.png', result)

# create masks and classification map
indexed = img.copy()
for i in range(k[1]):
                sample = cluster_centers[i]

                mask = cv2.inRange(result, sample, sample)

                if b[1] != 0:
                                if not b[1] % 2 != 0:
                                                b[1] += 1
                                mask = cv2.GaussianBlur(mask, (b[1], b[1]), 0)

                cv2.imwrite(f'{path}/mask{i}.png', mask)

                indexed[mask>0] = (i, i, i)

cv2.imwrite(f'{path}/index_map.png', indexed)

print('\nDone.\n')