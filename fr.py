# coding=utf-8

# --------------------------------
# Author: Tianxin Tse, Qianbo Inc.
# Update-Date: 2017-09-19
# --------------------------------

from construct_face import cf
import sys


def face_reconstruction(img_file):
    # initialize foler to store results
    cf.generate_init(img_file)

    print("\tConstructing face from iamge...")
    # generate intermediate files
    fg_file = cf.generate_fg(img_file)
    tri_file = cf.generate_tri(fg_file)

    # generate fbx and obj files
    cf.generate_fbx(tri_file)
    cf.generate_obj(tri_file)

    print("\n\t-----------------------------")
    print("\tFace Reconstruction Succeeds!")
    print("\t-----------------------------\n")


if __name__ == '__main__':
    """
    Command line need one argument: the image file
    """
    if len(sys.argv) != 2:
        print("Usage:\n"
              "\n\tfr <image.jpg>")
        exit()

    face_reconstruction(sys.argv[1])
