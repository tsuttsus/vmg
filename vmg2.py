import cv2 
import numpy as np 
from numba import jit
import matplotlib.pyplot as plt 
import matplotlib.cm as cm

#白->白黒
#黒->黒白

@jit()
def VerticalMoire(img,hpitch):
    result=np.zeros((img.shape[0],img.shape[1]))
    for y in range(0,img.shape[0]):
        for x in range(0,img.shape[1],hpitch*2):
            t=img[y][x]
            if t>120:
                for k in range(hpitch):
                    result[y][x+k]=255
                    result[y][x+hpitch+k]=0
            else:
                for k in range(hpitch):
                    result[y][x+k]=0
                    result[y][x+hpitch+k]=255
    return result

@jit()
def VerticalMoire2(img,hpitch):
    result=np.zeros((img.shape[0],img.shape[1]))
    result.fill(255)
    sample=np.zeros((img.shape[0],img.shape[1]//(hpitch*2)+1))
    sample2=sample.copy()

    for x in range(0,img.shape[1],hpitch*2):
        wcnt=12
        bcnt=12
        for y in range(0,img.shape[0]):
            if img[y][x]>120:
                sample[y][x//(hpitch*2)]=wcnt
                wcnt=wcnt+1
                bcnt=0
            else:
                sample[y][x//(hpitch*2)]=bcnt
                bcnt=bcnt+1
                wcnt=0
    
    for x in range(0,img.shape[1],hpitch*2):
        wcnt=12
        bcnt=12
        for y in range(img.shape[0]-1,-1,-1):
            if img[y][x]>120:
                sample2[y][x//(hpitch*2)]=wcnt
                wcnt=wcnt+1
                bcnt=0
            else:
                sample2[y][x//(hpitch*2)]=bcnt
                bcnt=bcnt+1
                wcnt=0
        
    for x in range(sample.shape[1]):
        for y in range(sample.shape[0]):
            if img[y][x*(2*hpitch)]>120:
                s=sample[y][x]
                if s<12:
                    for k in range(hpitch):
                        if x*(2*hpitch)+int(s/1)+k>img.shape[1]:
                            break
                        result[y][x*(2*hpitch)+int(s/1)+k]=0
                else:
                    for k in range(hpitch):
                        if x*(2*hpitch)+hpitch+k>img.shape[1]:
                            break
                        result[y][x*(2*hpitch)+hpitch+k]=0
            else:
                s=sample[y][x]
                if s<12:
                    for k in range(hpitch):
                        if x*(2*hpitch)+int(s/1)+k>img.shape[1]:
                            break
                        result[y][x*(2*hpitch)+hpitch-int(s/1)+k]=0
                else:
                    for k in range(hpitch):
                        if x*(2*hpitch)+k>img.shape[1]:
                            break
                        result[y][x*(2*hpitch)+k]=0
    return result

@jit()
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
    fn="test0.png"
    hpitch=12
    img=cv2.imread(fn,0)
    print("dd")
    
    array=np.zeros((img.shape[0],img.shape[1],4))
    ref_moire=VerticalRefMoire(array,hpitch)
    moire_graphy=VerticalMoire2(img,hpitch)
    print(type(moire_graphy))
    print(moire_graphy.shape)
    cv2.imwrite("ref3.png",ref_moire)
    cv2.imwrite("tes3.png",moire_graphy)