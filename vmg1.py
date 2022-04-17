import cv2 
import numpy as np 
from numba import jit

#@jit()
def VerticalMoire(img,hpitch):
    result=np.zeros((img.shape[0],img.shape[1]))
    for y in range(0,img.shape[0]):
        for x in range(0,img.shape[1],hpitch*2):
            t=img[y][x]
            if t>120:
                for k in range(hpitch):
                    if x+hpitch+k>=img.shape[1]:
                        break
                    result[y][x+k]=255
                    result[y][x+hpitch+k]=0
            else:
                for k in range(hpitch):
                    if x+hpitch+k>=img.shape[1]:
                        break
                    result[y][x+k]=0
                    result[y][x+hpitch+k]=255
    return result

#@jit()
def VerticalRefMoire(array,hpitch):
    for j in range(array.shape[0]):
        white=False
        for i in range(0,array.shape[1],hpitch):
            if white:
                for k in range(hpitch):
                    if i+k>=array.shape[1]:
                        break
                    array[j][i+k]=[255,255,255,0]
                white=False
            elif not white:
                for k in range(hpitch):
                    if i+k>=array.shape[1]:
                        break
                    array[j][i+k]=[0,0,0,255]
                white=True
    return array

if __name__=="__main__":
    fn="test1.png"
    hpitch=12
    img=cv2.imread(fn,0)
    
    array=np.zeros((img.shape[0],img.shape[1],4))
    ref_moire=VerticalRefMoire(array,hpitch)
    moire_graphy=VerticalMoire(img,hpitch)
    cv2.imwrite("ref3.png",ref_moire)
    cv2.imwrite("tes3.png",moire_graphy)
