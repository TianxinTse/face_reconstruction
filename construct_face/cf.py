# coding=utf-8

# --------------------------------
# Author: Tianxin Tse, Qianbo Inc.
# Update-Date: 2017-09-19
# --------------------------------
from face_landmarks_detection import fld
import os

# The parent folder of this file
PARENT_PATH = os.path.dirname(__file__) + os.path.sep + '..'

# The template for generating mesh
SDK = '/fg3/sdk/csamDefault33/HeadHires'

# Folder to store results: fg file, tri file, fbx file, etc
RESULT_FOLDER = '/results/'


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
    fg_file = PARENT_PATH + RESULT_FOLDER + fg_file

    # cmd command
    command = 'fg3pf photofit ' + fg_file + ' ' + image

    # execute command
    os.system(command)


def generate_head(fg_file):
    """
    Generate head mesh from fg file and templates

    :return: None
    """
    # get filename of fg file without extension
    result_filename = os.path.split(fg_file)[1].split('.')[0]

    # cmd command
    command = 'fg3 construct ' + \
              PARENT_PATH + SDK + ' ' + \
              PARENT_PATH + fg_file + ' ' + \
              PARENT_PATH + RESULT_FOLDER + result_filename

    # execute command
    os.system(command)
