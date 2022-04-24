#图像处理
#读取图片转为rgb565 字符串，并且写入test.txt
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np 
import re

def img2rgb():
    img = np.array(Image.open('2.jpg'))
    print(img.shape)
    width = img.shape[1]
    height = img.shape[0]
    enterCount = 0
    myfile = open("test.txt", "w")
    cString = " "
    myfile.write("/* Image Width:%dHeight:%d*/" %(width, height))
    myfile.write("\n")
    imgTest = np.zeros((height, width, 3))
    for i in range(0, height):
        for j in range(0, width):
            blueTemp = int(img[i,j,2]/8)
            redTemp = int(img[i,j,0]/4)
            greenTemp = int(img[i,j,1]/8)
            # rgb565Temp = "{:#06X}".format(blueTemp*(2**11) + redTemp*(2**5) + greenTemp)
            # TFT_eSPI官方写法
            rgb565Temp = "{:#06X}".format(((int(img[i,j,0]) & 0xF8) << 8) | ((int(img[i,j,1]) & 0xFC) << 3) | (int(img[i,j,2]) >> 3))
            imgTest[i,j,0] = redTemp*4
            imgTest[i,j,1] = greenTemp*8
            imgTest[i,j,2] = blueTemp*8
            imgTest[i,j,0] = img[i,j,0]
            imgTest[i,j,1] = img[i,j,1]
            imgTest[i,j,2] = img[i,j,2]
            cString += rgb565Temp
            cString += " "
            if(enterCount%width == width-1):
                cString += "\n"
            enterCount = enterCount+1
    cString += " "
    myfile.write(cString)
    # 在电脑上预览原图
    # plt.imshow(imgTest/255)
    # plt.show()
    return cString,width, height

def rgb2img(rgbstr,w,h):
    match = re.findall(r"0[x,X][0-9a-fA-F]{4}",rgbstr,re.I)
    imgTest = np.zeros((h, w, 3))
    # print(match)
    for i in range(h):
        for j in range(w):
            blueTemp = (int(match[i*w+j],16)& 0x001f)
            redTemp = (int(match[i*w+j],16)& 0xf800) >> 8
            greenTemp =(int(match[i*w+j],16)& 0x07e0)>>3
            # rgb565Temp = "{:#06X}".format(blueTemp*(2**11) + redTemp*(2**5) + greenTemp)
            # TFT_eSPI官方写法
            # rgb565Temp = "{:#06X}".format(((int(img[i,j,0]) & 0xF8) << 8) | ((int(img[i,j,1]) & 0xFC) << 3) | (int(img[i,j,2]) >> 3))
            imgTest[i,j,0] = redTemp
            imgTest[i,j,1] = greenTemp
            imgTest[i,j,2] = blueTemp
    plt.imshow(imgTest/255)
    plt.show()        



if __name__=="__main__":
    res,w,h=img2rgb()
    rgb2img(res,w,h)