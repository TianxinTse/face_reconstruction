# coding=utf-8

# --------------------------------
# Author: Tianxin Tse, Qianbo Inc.
# Update-Date: 2017-09-19
# --------------------------------

from construct_face import cf
import os
import sys


def face_reconstruction(img_file):
    fg_file = cf.generate_fg(img_file)
    tri_file = cf.generate_tri(fg_file)
    cf.generate_fbx(tri_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage:\n"
              "\n\tfr <image.jpg>")
        exit()

    face_reconstruction(sys.argv[1])
