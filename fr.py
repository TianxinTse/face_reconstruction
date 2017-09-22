# coding=utf-8

# --------------------------------
# Author: Tianxin Tse, Qianbo Inc.
# Update-Date: 2017-09-19
# --------------------------------

from construct_face import cf
import sys
import os


def face_reconstruction(img_file):
    # initialize foler to store results
    folder = cf.generate_init(img_file)

    print("\tConstructing face from iamge...")
    # generate intermediate files
    fg_file = cf.generate_fg(img_file)
    tri_file = cf.generate_tri(fg_file)

    # generate fbx and obj files
    cf.generate_fbx(tri_file)
    cf.generate_obj(tri_file)

    # generate zip package of .obj .fbx and .png files
    cf.build_zip_package(folder, 'fbx&obj&png.zip')

    print("\n\t-----------------------------")
    print("\tFace Reconstruction Succeeds!")
    print("\t-----------------------------\n")

    foldername = os.path.split(img_file)[1].split('.')[0]
    common_path = 'E:\\computer-vision\\human-face\\'

    src = common_path + 'face-reconstruction\\results\\' + foldername
    dst = common_path + \
        'FaceModeling\\src\\main\\webapp\\images\\download\\' + \
        foldername + '\\'

    command = 'xcopy ' + src + ' ' + dst + ' /E /Y /Q'
    print(command)
    os.system(command)


if __name__ == '__main__':
    """
    Command line need one argument: the image file
    """
    print(sys.argv[1])
    if len(sys.argv) != 2:
        print("Usage:\n"
              "\n\tfr <image.jpg>")
        exit()

    face_reconstruction(sys.argv[1])
