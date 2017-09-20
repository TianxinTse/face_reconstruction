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


def generate_fg(img_file):
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

    # return name of fg file
    return fg_file


def generate_tri(fg_file):
    """
    Generate head mesh from fg file and templates

    :param fg_file:
    :return: None
    """
    # get filename
    filename = os.path.split(fg_file)[1].split('.')[0]
    tri_file = filename + '.tri'
    fg_file = filename + '.fg'

    # cmd command
    command = 'fg3 construct ' + \
              PARENT_PATH + SDK + ' ' + \
              PARENT_PATH + RESULT_FOLDER + fg_file + ' ' + \
              PARENT_PATH + RESULT_FOLDER + filename

    # execute command
    os.system(command)

    # return name of tri file
    return tri_file


def generate_fbx(tri_file):
    """
    Generate fbx file from mesh file.
    :param tri_file: mesh file
    :return: None
    """
    # build result filename
    filename = os.path.split(tri_file)[1].split('.')[0]
    fbx_file = filename + '.fbx'
    tri_file = filename + '.tri'

    # cmd command
    command = 'fg3 meshops convert ' + \
              PARENT_PATH + RESULT_FOLDER + tri_file + ' ' + \
              PARENT_PATH + RESULT_FOLDER + fbx_file

    # execute command
    os.system(command)
