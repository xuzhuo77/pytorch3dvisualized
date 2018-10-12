# -*- coding: utf-8 -*-



from PIL import Image
import numpy as np 
from matplotlib import cm
import matplotlib.pyplot as plt
def makeimage(array):
    img=Image.fromarray(np.array(array))
    img.show()


def color_jet():
    colormap_int = np.zeros((256, 3), np.uint8)
    colormap_float = np.zeros((256, 3), np.float)
    
    for i in range(0, 256, 1):
       colormap_float[i, 0] = cm.jet(i)[0]
       colormap_float[i, 1] = cm.jet(i)[1]
       colormap_float[i, 2] = cm.jet(i)[2]
 
       colormap_int[i, 0] = np.int_(np.round(cm.jet(i)[0] * 255.0))
       colormap_int[i, 1] = np.int_(np.round(cm.jet(i)[1] * 255.0))
       colormap_int[i, 2] = np.int_(np.round(cm.jet(i)[2] * 255.0))
      
    return colormap_int


def gray2color(gray_array,color_map):
    rows,cols=gray_array.shape
    color_array=np.zeros((rows, cols,3), np.uint8)
    
    
    
    for i in range(rows):
        for jn in range(cols):
            color_array[i, jn] = color_map[int(gray_array[i,jn])]
    
    color_image = Image.fromarray(color_array)
 
    return color_image

def colormap(gray_array):
    jet_map=color_jet()
    
    return gray2color(gray_array, jet_map)
def test_colormap():
    array=np.random.rand(20,20)
    plt.imshow(colormap(array))
    plt.show()