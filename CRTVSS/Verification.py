import random
import os
from PIL import Image
from Vss_share import Binary_transform1

def verification(k, n, p,screen_lowest_xor_num, secret_image_name,verification_image_name):
    image_choice_list = []
    list_choice = range(1,n+1)
    num_choice =random.sample(list_choice, 2)
    print(num_choice)
    random_image = Image.open("./shares_ideal/"+secret_image_name+"_share_k"+str(k)+"_n"+str(n)+"_p"+str(p)+"_s"+str(screen_lowest_xor_num)+"/Share"+str(num_choice[0])+".bmp", 'r')
    binary_shadow_image_size = random_image.size
    print(binary_shadow_image_size)
    secret_shadow_binary_list_1 = [[0 for i in range(binary_shadow_image_size[0])] for j in range(binary_shadow_image_size[1])]
    secret_shadow_binary_list_2 = [[0 for i in range(binary_shadow_image_size[0])] for j in range(binary_shadow_image_size[1])]
    ver_construct_image = Image.new('L', binary_shadow_image_size)
    for i in range(2):
        image_choice = Image.open("./shares_ideal/"+secret_image_name+"_share_k"+str(k)+"_n"+str(n)+"_p"+str(p)+"_s"+str(screen_lowest_xor_num)+"/Share"+str(num_choice[i])+".bmp")
        image_choice_list.append(image_choice)
    secret_shadow_binary_list = [secret_shadow_binary_list_1,secret_shadow_binary_list_2]
    for r in range(2):
        for i in range(binary_shadow_image_size[0]):
            for j in range(binary_shadow_image_size[1]):
                pixel = image_choice_list[r].getpixel((i,j))
                pixel_bin = "{:08b}".format(pixel)
                lowbit = int(pixel_bin[7])
                for index in range(7-screen_lowest_xor_num+1,7):
                    lowbit = lowbit ^ int(pixel_bin[index])
                secret_shadow_binary_list[r][i][j] = lowbit
    for i in range(binary_shadow_image_size[0]):
        for j in range(binary_shadow_image_size[1]):
            ver_construct_image.putpixel((i,j),Binary_transform1(secret_shadow_binary_list_1[i][j] ^ secret_shadow_binary_list_2[i][j]))
    path = '.\\verification_ideal\\' + verification_image_name+'_k{0}_n{1}_p{2}_s{3}\\'.format(k, n, p,screen_lowest_xor_num)
    if not os.path.exists(path):
        os.makedirs(path)
    ver_construct_image.save(path + 'verification.bmp', 'BMP')

verification(2,4,131,8,"lena","hit")