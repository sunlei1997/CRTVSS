import random


def Binary_transform(num):                   #提取最低有效位
    if num == 255:
        return 1
    elif num == 0:
        return 0

def Binary_transform1(num):                   #将二值图像输出
    if num == 0:
        return 0
    elif num == 1:
        return 255

def VSS_Repeat(Bpixel, k, n):                 #计算得到二值图像每个像素位的n个值，用作分享。每个像素计算的结果储存在SharedPixels中
    SharedPixels = []
    XorResult = 0
    for i in range(k):                        #循环k次，得到k个分享值。
        NewPixel = random.choice([0, 1])
        SharedPixels.append(NewPixel)
        XorResult = XorResult ^ NewPixel
    if XorResult != Bpixel:                   #这一步是为了确保两两异或能够恢复出原像素值
        RanSerial = random.choice(range(k))
        SharedPixels[RanSerial] = SharedPixels[RanSerial] ^ 1
    for i in range(n-k):                      #循环得到后n-k个分享值
        if (i + 1) % k != 0:
            SharedPixels.append(SharedPixels[(i + 1) % k -1])
        else:
            SharedPixels.append(SharedPixels[k-1])
    # random.shuffle(SharedPixels)
    return SharedPixels



