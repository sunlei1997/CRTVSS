import os
from PIL import Image
from Vss_share import Binary_transform1
from Vss_share import Binary_transform

def ver_dealer(k,n,p,s):
    verification_binary_image = Image.open("./dealer_binary_verification_image/_binary_share_k{0}_n{1}_p{2}_s{3}/".format(k,n,p,s)+"dealer_verification.bmp", 'r')
    image_size = verification_binary_image.size
    binary_share_image_list = []
    ver_construct_image_list = []
    for i in range(n):
        binary_share_image = Image.open("./binary_shares_ideal/lena_binary_share_k{0}_n{1}_p{2}_s{3}".format(k,n,p,s)+"/Binary_share"+str(i+1)+".bmp", 'r')
        binary_share_image_list.append(binary_share_image)
        ver_construct_image = Image.new('L', image_size)
        ver_construct_image_list.append(ver_construct_image)
    for index in range(n):
        for i in range(image_size[0]):
            for j in range(image_size[1]):
                verification_binary_image_value = verification_binary_image.getpixel((i,j))
                binary_share_image_value = binary_share_image_list[index].getpixel((i,j))
                ver_construct_image_list[index].putpixel((i,j),Binary_transform1(Binary_transform(verification_binary_image_value) ^ Binary_transform(binary_share_image_value)))
    path = '.\\verification_dealer\\' + 'hit' + '_k{0}_n{1}_p{2}_s{3}\\'.format(k, n, p,s)
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(n):
        ver_construct_image_list[i].save(path + 'verification'+str(i)+'.bmp', 'BMP')

if __name__ == '__main__':
    ver_dealer(3,4,131,8)