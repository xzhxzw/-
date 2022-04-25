"""
参数定义
---------------------------------------------------------------
设备地址：
    按照com端口号?或者按照识别到的串口的编号
图像类型:    
    0x01: 原始RGB565像素数据
    0x02: BMP格式图片
    0x03: PNG格式图片
    0x04: JPEG格式图片
包长度：
    最终计算(pack函数实现拼接)
分辨率(宽高):    
    240*320/480*640
数据传送顺序：  
    多于1字节使用小数端
校验：
    CRC-16
    多项式 X^16+X^15+X^2+1
    多项式 POLY(Hex)8005
    初始值 INIT(Hex)FFFF
    结果异或值 XOROUT(Hex)0000

---------------------------------------------------------------

包结构：
    指令包：
        字节数	    4bytes	    1bytes	    4bytes	    1bytes	    1bytes	    2bytes	    2bytes	    2 bytes
        名称	    包头	    设备地址	 包长度	      指令	      图像格式	    宽	        高	        校验
        内容	    0x59485A53	xxxx	    xxxx	    0x01	    xxxx	    xxxx	    xxxx	    xxxx
    应答包：
        字节数	    4bytes	    1bytes	    4bytes	    1bytes	    1bytes	    2bytes
        名称	    包头	    设备地址	 包长度	      指令	      确认码	  校验
        内容	    0x59485A53	xxxx	    xxxx	    0x00	    xxxx	    xxxx
    数据包：
        字节数	    4bytes	    1bytes	    4bytes	    1bytes	    Nbytes	    2bytes
        名称	    包头	    设备地址	 包长度	      指令	      图像数据	   校验
        内容	    0x59485A53	xxxx	    xxxx	    0x02	    xxxx	    xxxx

待定包结构：
    上位机主动读写数据？
"""

def calc_crc(data):
    """
        校验位计算，返回十六进制字符串
    """
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return hex(((crc & 0xff) << 8) + (crc >> 8))

def check(data):
    """
        对于接收到的数据进行包检索以及信息提取
        三种包整合
    """
    import re

    pattern = r'59485a53'                      # 定义分隔符
    result = re.split(pattern, data) # 以pattern的值 分割字符串
    for each in result:
        print(each)#各个包除包头外的内容
        pass
        #TODO:依次检测包内容判断相关信息


class orderpck:
    """
        指令包
        addr:设备编号 int
        imageset:四种图片类型 int传入
        width:图像宽 int传入
        length:图像高 int传入
    """
    def __init__(self,addr,imageset,width,height):
        self.addr=addr
        self.imageset=imageset
        self.width=width
        self.height=height
        self.pck=bytearray.fromhex("59485A53")

    def pack(self):
        self.pck += bytearray(int(self.addr).to_bytes(1, byteorder='big'))#地址
        self.pck += bytearray(int(17).to_bytes(4, byteorder='big'))#长度
        self.pck += bytearray(int(1).to_bytes(1, byteorder='big'))#指令
        self.pck += bytearray(int(self.imageset).to_bytes(1, byteorder='big'))#图像格式设置
        self.pck += bytearray(int(self.width).to_bytes(2, byteorder='big'))#图像宽设置
        self.pck += bytearray(int(self.height).to_bytes(2, byteorder='big'))#图像高设置，注意选择方式从两种分辨率选择
        clc=calc_crc(self.pck)
        print(clc)
        clc=clc[2:6]
        self.pck += bytearray.fromhex(clc)
        return self.pck


class replypck:
    """
        数据包或者指令包的应答包
        addr:设备编号 int
        确认码:
            0x00:指令执行完毕或 OK
            0x01:数据包接收错误
            0x02:没有这个寄存器
            0x03~0xFF:保留
    """
    def __init__(self,addr,reply):
        self.addr=addr
        self.reply=reply
        self.pck=bytearray.fromhex("59485A53")

    def pack(self):
        self.pck += bytearray(int(self.addr).to_bytes(1, byteorder='big'))#地址
        self.pck += bytearray(int(13).to_bytes(4, byteorder='big'))#长度
        self.pck += bytearray(int(2).to_bytes(1, byteorder='big'))#指令
        self.pck += bytearray(int(self.reply).to_bytes(1, byteorder='big'))#确认码
        clc=calc_crc(self.pck)
        print(clc)
        clc=clc[2:6]
        self.pck += bytearray.fromhex(clc)
        return self.pck



class datapck:
    """
        数据包
        addr:设备编号 int
        data:Nbytes 按帧(16bit)小数端形式构建字节数组，即每一帧按照小数端，传入形式
    """
    def __init__(self,addr,data):
        self.addr=addr
        self.data=data
        self.pck=bytearray.fromhex("59485A53")

    def pack(self):
        self.pck += bytearray(int(self.addr).to_bytes(1, byteorder='big'))#地址
        self.pck += bytearray(int(17).to_bytes(4, byteorder='big'))#长度
        self.pck += bytearray(int(1).to_bytes(2, byteorder='big'))#指令
        self.pck += bytearray(int(self.data).to_bytes(1, byteorder='big'))#数据
        clc=calc_crc(self.pck)
        print(clc)
        clc=clc[2:6]
        self.pck += bytearray.fromhex(clc)
        return self.pck



#TODO：实现接收包后的识别，传入格式，用串口读入后的形式？

if __name__ == '__main__':
    pck=orderpck(1,1,240,320)
    result=pck.pack()
    for i in range(len(result)):
        print("%02x"%result[i],end=" ") 
    print("")
    check("59485a530100000011010100f00140b4ec59485a535151651651")
