# coding=utf-8

# --------------------------------
# Author: Tianxin Tse, Qianbo Inc.
# Update-Date: 2017-09-19
# --------------------------------

from face_landmarks_detection import fld
import os
import zipfile

# The parent folder of this file
PARENT_PATH = os.path.dirname(__file__) + os.path.sep + '..'

# The template for generating mesh
SDK = '/fg3/sdk/csamDefault33/HeadHires'

# Sources folder: imgs and xmls
SOURCE_FOLDER = '/sources/'

# Folder to store results: fg file, tri file, fbx file, etc
RESULT_FOLDER = '/results/'

# Image specific folder
UNIQUE_FOLDER = ''


def generate_init(img_file):
    """
    Some initial operations

    :param img_file: image file
    :return: None
    """
    print("\tInitializing...", end='')

    filename = os.path.split(img_file)[1].split('.')[0]
    dirname = PARENT_PATH + RESULT_FOLDER + filename + '/'

    if not os.path.exists(dirname):
        os.mkdir(dirname)

    global UNIQUE_FOLDER
    UNIQUE_FOLDER = dirname

    print('\tOK')
    # print(UNIQUE_FOLDER)
    return UNIQUE_FOLDER


def generate_fg(img_file):
    """
    Generate fg file from an image and a corresponding xml file

    :param img_file: image file
    :return: None
    """
    print("\tGenerating fg file...")

    # get landmarks of face
    img_file = os.path.split(img_file)[1]
    image = PARENT_PATH + SOURCE_FOLDER + img_file
    # image = os.path.abspath(os.getcwd() + img_file)
    shape = fld.get_landmarks(image)

    # get critical points
    critical_points = fld.get_critical_points(shape)

    # generate xml file
    fld.generate_xml_marks(image, critical_points)

    # generate fg file
    # filename
    fg_file = os.path.split(image)[1].split('.')[0] + '.fg'

    # cmd command
    command = 'fg3pf photofit ' + UNIQUE_FOLDER + fg_file + ' ' + image

    # execute command
    os.system(command)

    # return name of fg file
    print('\tfg file generated...\tOK')
    return fg_file


def generate_tri(fg_file):
    """
    Generate head mesh from fg file and templates

    :param fg_file: fg file
    :return: None
    """
    print("\tGenerating tri file...", end='')

    # get filename
    filename = os.path.split(fg_file)[1].split('.')[0]
    tri_file = filename + '.tri'
    fg_file = filename + '.fg'

    # cmd command
    command = 'fg3 construct ' + \
              PARENT_PATH + SDK + ' ' + \
              UNIQUE_FOLDER + fg_file + ' ' + \
              UNIQUE_FOLDER + filename

    # execute command
    os.system(command)

    # return name of tri file
    print('\tOK')
    return tri_file


def generate_fbx(tri_file):
    """
    Generate fbx file from tri file.

    :param tri_file: tri file
    :return: None
    """
    print("\tGenerating fbx file...", end='')

    # build result filename
    filename = os.path.split(tri_file)[1].split('.')[0]
    fbx_file = filename + '.fbx'
    tri_file = filename + '.tri'

    # cmd command
    command = 'fg3 meshops convert ' + \
              UNIQUE_FOLDER + tri_file + ' ' + \
              UNIQUE_FOLDER + fbx_file

    # execute command
    os.system(command)
    print('\tOK')


def generate_obj(tri_file):
    """
    Generate obj file from tri file

    :param tri_file: tri file
    :return: None
    """
    print("\tGenerating obj file...", end='')

    # build result filename
    filename = os.path.split(tri_file)[1].split('.')[0]
    obj_file = filename + '.obj'
    tri_file = filename + '.tri'
    bmp_file = filename + '.bmp'

    # cmd command
    command = 'fg3 triexport ' + \
              UNIQUE_FOLDER + obj_file + ' ' + \
              UNIQUE_FOLDER + tri_file + ' ' + \
              UNIQUE_FOLDER + bmp_file

    # execute command
    os.system(command)
    print('\tOK')


def build_zip_package(dirname, zipfilename):
    """
    Build a .zip package for users to download
    Package contains .obj .fbx and .png files

    :param dirname: directory to be compressed
    :param zipfilename: output name of zip file
    """
    print("\tGenerating zip package file...", end='')

    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                ext = name.split('.')[1]
                # Only .obj .fbx and .png files
                if ext != 'obj' and ext != 'fbx' and ext != 'png':
                    continue
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(dirname + zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)

    zf.close()

    print('\tOK')
