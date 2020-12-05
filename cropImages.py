'''
作用：根据用户给定分辨率，将给定目录下的每张大图裁剪成多张小图并储存
变量：分辨率STRIDE, 输入目录FILE_DIR，输出目录OUTPUT_DIR
'''
import cv2
import math
import os

STRIDE = 512
FILE_DIR = r'/home/alex/Desktop/work/noneProposed/Pleiades/labels/'
OUTPUT_DIR = r'//home/alex/Desktop/work/proposed/Pleiades/labels/'


# mission: return sub dirs of the FILE_DIR given by user
# return: a 1D list,including names of sub dirs
def file_name(file_dir):
    dirs = os.listdir(file_dir)
    return dirs


# mission: load images into a list
# return: a 3D list,including the images; a 1D list, including names of sub dirs
def loadImage(file_dir):
    dirs = file_name(file_dir)

    imgs_list = []
    for name in dirs:
        img = cv2.imread(FILE_DIR + name, -1)
        imgs_list.append(img)

    print('the total number of images : {}'.format(len(imgs_list)))
    return imgs_list, dirs


# mission: compute the number of crop pics of the image according to STRIDE
# return: 3 int number
def computeNumOfPics(row, col):
    num_of_row_pic = math.floor(row / STRIDE)
    num_of_col_pic = math.floor(col / STRIDE)
    num_of_total_pic = num_of_row_pic * num_of_col_pic
    print('num_of_total_pic: {}\tnum_of_row_pic:{}\tnum_of_col_pic:{}'.format(num_of_total_pic, num_of_row_pic,
                                                                              num_of_col_pic))
    return num_of_total_pic, num_of_row_pic, num_of_col_pic


# mission: to crop the image into several pics according to the num of pics
# return: a 3D list,including all pics that has been cropped
def cropImage(img, num_of_row_pic, num_of_col_pic):
    pics_list = []  # to save the number of the pics that can be cropped from the image
    col_coordinates_list = []  # to save the coordinates information of col
    row_coordinates_list = []  # to save the coordinates information of row

    for i in range(num_of_col_pic + 1):
        col_coordinates_list.append(i * STRIDE)

    for i in range(num_of_row_pic + 1):
        row_coordinates_list.append(i * STRIDE)

    print('row_coordinates_list:    {}\ncol_coordinates_list:    {}'.format(row_coordinates_list, col_coordinates_list))

    for i in range(len(row_coordinates_list) - 1):
        for j in range(len(col_coordinates_list) - 1):
            pics_list.append(img[row_coordinates_list[i]:row_coordinates_list[i + 1],
                             col_coordinates_list[j]:col_coordinates_list[j + 1]])

    return pics_list


# mission: save pics into files
def savePics(pics_list, name):
    i = 0
    for pic in pics_list:
        cv2.imwrite(OUTPUT_DIR + '%s_%d.tif' % (name.replace('.tif', ''), i), pic)
        i += 1


if __name__ == '__main__':
    # load the image
    imgs_list, dirs = loadImage(FILE_DIR)

    i = 0
    for img in imgs_list:
        # compute the num of pics in the image
        print('%s' % dirs[i])
        num_of_total_pic, num_of_row_pic, num_of_col_pic = computeNumOfPics(img.shape[0], img.shape[1])

        # crop the image into pics
        pics_list = cropImage(img, num_of_row_pic, num_of_col_pic)

        # save the pics
        savePics(pics_list, dirs[i])

        i += 1