import math
import random
import os
from PIL import Image
from constants import *
import numpy as np


def Multiple_Inv(Mi, mi):
    for w in range(mi):
        if (Mi * w) % mi == 1:
            return w

def CRT_recovering(shares_list, mlist, T, p):
    Mi_list = []
    Minv_list = []
    M = 1
    N = 1
    for i in range(len(mlist)):
        M = M * mlist[i]
    for j in range(len(mlist)):
        Mi_list.append(M / mlist[j])  #计算Mi
        Minv_list.append(Multiple_Inv(Mi_list[j], mlist[j]))   #计算Mi模mi的逆元
    print(Mi_list)
    print(M)
    print(Minv_list)
    for i in range(len(mlist)):
        print(Minv_list[i] * Mi_list[i])
    Shares = []
    rec_shares = ''
    for share in shares_list:
        Shares.append(Image.open(share, 'r'))
        rec_shares = rec_shares + share[-5]
    recover_image = Image.new('L', Shares[0].size)

    for i in range(Shares[0].size[0]):
        for j in range(Shares[0].size[1]):
            if (i+j) % 2 == 0:
                flag = 0
            else:
                flag = 1
            share_pixel_list = []
            for Share in Shares:
                share_pixel_list.append(Share.getpixel((i, j)))
            # rec_pixel = CRTintOE_pixel_recover(share_pixel_list, M, Mi_list, Minv_list, p)
            rec_pixel = CRTbyYan_pixel_recover(share_pixel_list, M, T, Mi_list, Minv_list, p)
            # rec_pixel = CRTideal_pixel_recover(share_pixel_list, M, Mi_list, Minv_list, p, flag)
            recover_image.putpixel((i, j), rec_pixel)

    recover_image.save(shares_list[0][:-10] + 'rec' + rec_shares + '.bmp', 'BMP')



if __name__ == '__main__':
    k = 3
    n = 4
    p = 131
    s = 8
    key = '({0}, {1})'.format(n, p)
    mlist = mlist_dir[key]

    M = 1
    N = 1
    for i in range(k):
        M = M * mlist[i]
    for j in range(n-k+1, n):
        N = N * mlist[j]
    minA = math.ceil(N / p)
    maxA = math.floor(M / p - 1)
    T = int((math.floor(M / p - 1) - math.ceil(N / p)) / 2 + math.ceil(N / p))

    list_range = range(1,n+1)
    num = random.sample(list_range,k)
    num.sort()
    print(num)

    shares_list = []
    mylist = []
    for i in range(k):
        shares_list.append('.\\shares_ideal\\' + 'lena_share_k{0}_n{1}_p{2}_s{3}\\'.format(k, n, p, s) + "Share" + str(num[i])+".bmp")
        mylist.append(mlist[num[i]-1])

    CRT_recovering(shares_list, mylist, T, p)

