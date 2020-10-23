import math
import numpy
import random
import os
from PIL import Image
from constants import *
from Vss_share import VSS_Repeat
from Vss_share import Binary_transform1
from Vss_share import Binary_transform

def CRTbySun_pixel_sharing(secret_image_pixel, verification_image_pixel, mlist, T, minA, maxA, p, n, screen_lowest_xor_num):
    binary_shadow_value = VSS_Repeat(Binary_transform(verification_image_pixel), 2, n+1)
    Share_pixel_list = []
    Share_pixel_binary_list = []
    x = secret_image_pixel
    if (x >= p):
        A = random.randint(minA, T - 1)
        y = x - p + A * p
    else:
        A = random.randint(T + 1, maxA)
        y = x + A * p
    for i in range(n):
        remainer = y % mlist[i]
        Share_pixel_list.append(remainer)
        remainer = "{:08b}".format(remainer)
        lowbit = int(remainer[7])
        for j in range(7-screen_lowest_xor_num+1,7):
            lowbit = lowbit ^ int(remainer[j])
        Share_pixel_binary_list.append(lowbit)
    if (binary_shadow_value[:-1].count(1) == Share_pixel_binary_list.count(1)):
        return (Share_pixel_list,Share_pixel_binary_list,binary_shadow_value[-1])
    else:
        return False


def CRT_sharing(secret_image_path, verification_image_path, mlist, k, n, p, screen_lowest_xor_num):
    global tag
    M = 1
    N = 1
    for i in range(k):
        M = M * mlist[i]
    for j in range(n-k+1, n):
        N = N * mlist[j]
    minA = math.ceil(N / p)
    maxA = math.floor(M / p - 1)
    T = int((math.floor(M / p - 1) - math.ceil(N / p)) / 2 + math.ceil(N / p))
    secret_image = Image.open(secret_image_path, 'r')
    verification_image = Image.open(verification_image_path,"r")
    img_size = secret_image.size
    Shares = []
    Binary_shares = []
    Dealer_verification = Image.new("L",img_size)
    for i in range(n):
        Shares.append(Image.new('L', img_size))
        Binary_shares.append(Image.new("L",img_size))

    for i in range(img_size[0]):
        for j in range(img_size[1]):
            sec_pixel = secret_image.getpixel((i, j))
            ver_pixel = verification_image.getpixel((i, j))
            while(True):
                share_pixel_list = CRTbySun_pixel_sharing(sec_pixel, ver_pixel, mlist, T, minA, maxA, p, n, screen_lowest_xor_num)
                if share_pixel_list != False:
                    tag += 1
                    for share_index in range(len(share_pixel_list[0])):
                        Shares[share_index].putpixel((i, j), share_pixel_list[0][share_index])
                        Binary_shares[share_index].putpixel((i,j), Binary_transform1(share_pixel_list[1][share_index]))
                    Dealer_verification.putpixel((i,j),Binary_transform1(share_pixel_list[2]))
                    break
                else:
                    tag += 1
                    continue
    path = '.\\shares_ideal\\' + secret_image_path[:-4] + '_share_k{0}_n{1}_p{2}_s{3}\\'.format(k, n, p, screen_lowest_xor_num)
    if not os.path.exists(path):
        os.makedirs(path)
    seq = 0
    for Share in Shares:
        seq = seq + 1
        Share.save(path + 'Share{0}.bmp'.format(seq), 'BMP')
    path = '.\\binary_shares_ideal\\' + secret_image_path[:-4] + '_binary_share_k{0}_n{1}_p{2}_s{3}\\'.format(k, n, p, screen_lowest_xor_num)
    if not os.path.exists(path):
        os.makedirs(path)
    seq = 0
    for Share in Binary_shares:
        seq = seq + 1
        Share.save(path + 'Binary_share{0}.bmp'.format(seq), 'BMP')
    path = '.\\dealer_binary_verification_image\\' + '_binary_share_k{0}_n{1}_p{2}_s{3}\\'.format(k, n, p, screen_lowest_xor_num)
    if not os.path.exists(path):
        os.makedirs(path)
    seq = 0
    Dealer_verification.save(path + 'dealer_verification.bmp','BMP')

if __name__ == '__main__':
    tag = 0   #计算筛的次数
    k = 2     #门限
    n = 4     #参与者的数量
    p = 131   #CRT应用于SIS中的一个参数
    s = 8    #最低多少位异或来筛选
    key = '({0}, {1})'.format(n, p)
    mlist = mlist_dir[key]
    print(mlist)
    sec_image = 'lena.bmp'
    ver_image = 'hit.bmp'
    CRT_sharing(sec_image, ver_image, mlist, k, n, p, s)
    print(tag)
