# coding=utf-8

# --------------------------------
# Author: Tianxin Tse, Qianbo Inc.
# Update-Date: 2017-09-19
# --------------------------------
from face_landmarks_detection import fld
import os

# The parent folder of this file
PARENT_PATH = os.path.dirname(__file__) + os.path.sep + '..'


def generate_fg_file(img_file):
    """
    Generate fg file from an image and a corresponding xml file

    :return: None
    """
    # get landmarks of face
    image = os.path.abspath(os.getcwd() + img_file)
    shape = fld.get_landmarks(image)
    # get critical points
    critical_points = fld.get_critical_points(shape)
    # generate xml file
    fld.generate_xml_marks(image, critical_points)

    # generate fg file
    # filename
    fg_file = os.path.split(image)[1].split('.')[0] + '.fg'
    # filename with path
    fg_file = PARENT_PATH + '/results/' + fg_file
    # cmd command
    command = 'fg3pf photofit ' + fg_file + ' ' + image
    # execute command
    os.system(command)
