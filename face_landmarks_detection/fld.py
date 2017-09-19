# coding=utf-8

# --------------------------------
# Author: Tianxin Tse, Qianbo Inc.
# Update-Date: 2017-09-19
# --------------------------------

import sys
import os
import dlib
from skimage import io


# The parent folder of this file
PARENT_PATH = os.path.dirname(__file__) + os.path.sep + '..'
# The sample image for testing
TEST_IMG = PARENT_PATH + '/imgs/ldh.jpg'
# The predictor model
PREDICTOR_MODEL = PARENT_PATH + '/models/predic.dat'


def get_landmarks(img_file=TEST_IMG, predic_path=PREDICTOR_MODEL):
    """
    Use predict_model to detect face in img, and return the landmarks.
    Default values for parameters can be changed.

    :param img: A jpg image that contains a face.
    :param predict_model: The model for predicting face.
    :return: landmarks, a dlib.full_object_detection object
    """
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_MODEL)
    img = io.imread(img_file)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)

    # we just need one face
    if len(dets) != 1:
        print("Error:\n"
              "\tMultiple faces modeling not supported.\n"
              "\tPlease specify an image with exactly one face.\n")
        exit()

    shape = predictor(img, dets[0])

    return shape


def get_critical_points(shape):
    """
    Get critical points for reconstructing a 3D face model

    :param shape: full_object_detection object of dlib
    :return: A list of critical points
    """
    critical_points = []

    # We need 11 critical points to reconstruct a 3D model for a face

    # point 1  -- location of left ear
    critical_points.append([shape.part(1).x, shape.part(1).y])

    # point 15 -- location of right ear
    critical_points.append([shape.part(15).x, shape.part(15).y])

    # point 4  -- location of left cheek
    critical_points.append([shape.part(4).x, shape.part(4).y])

    # point 12 -- location of right cheek
    critical_points.append([shape.part(12).x, shape.part(12).y])

    # point 48 --  left corner of the mouth
    critical_points.append([shape.part(48).x, shape.part(48).y])

    # point 54 --  right corner of the mouth
    critical_points.append([shape.part(54).x, shape.part(54).y])

    # point 8  -- location of chin
    critical_points.append([shape.part(8).x, shape.part(8).y])

    # points 36 to 41 for calculating the location of left eye
    sum_x = sum([shape.part(i).x for i in range(36, 42)])
    sum_y = sum([shape.part(i).y for i in range(36, 42)])
    critical_points.append([int(sum_x / 6.0 + 0.5), int(sum_y / 6.0 + 0.5)])

    # points 42 to 47 for calculating the location of left eye
    sum_x = sum([shape.part(i).x for i in range(42, 48)])
    sum_y = sum([shape.part(i).y for i in range(42, 48)])
    critical_points.append([int(sum_x / 6.0 + 0.5), int(sum_y / 6.0 + 0.5)])

    # points 30 to 35 for calculating the location of two sides of nose
    avg_x_interval = int((shape.part(35).x - shape.part(31).x) / 5.0 + 0.5)
    avg_y = int(sum([shape.part(i).y for i in range(31, 36)]) / 5.0 + 0.5)

    # height of sides of nose
    nose_height = int((shape.part(30).y + avg_y) / 2.0 + 0.5)

    # left side of nose
    critical_points.append([shape.part(31).x - avg_x_interval, nose_height])

    # right side of nose
    critical_points.append([shape.part(35).x + avg_x_interval, nose_height])

    return critical_points


def generate_xml_marks(img_file, critical_points):
    """
    Use critical points of face to generate a bpt.xml file

    :param img: A jpg image that contains a face.
    :param critical_points: A list containing 11 points.
    :return: None
    """
    # load template xml file
    template_xml = PARENT_PATH + '/xmls/template.xml'
    f_template = open(template_xml)
    lines = f_template.readlines()
    f_template.close()

    # the first point
    lines.append('\t<item class_id="1" tracking_level="0" version="0">\n')
    point = critical_points.pop()
    lines.append('\t\t<column>' + str(point[0]) + '</column>\n')
    lines.append('\t\t<row>' + str(point[1]) + '</row>\n')
    lines.append('\t</item>\n')

    # the rest of points
    while len(critical_points) > 0:
        lines.append('\t<item>\n')
        point = critical_points.pop()
        lines.append('\t\t<column>' + str(point[0]) + '</column>\n')
        lines.append('\t\t<row>' + str(point[1]) + '</row>\n')
        lines.append('\t</item>\n')

    lines.append('</val>\n')
    lines.append('</boost_serialization>\n')

    # write to result
    result_xml = os.path.split(img_file)[1].split('.')[0] + '.bpt.xml'
    result_xml = PARENT_PATH + '/xmls/results/' + result_xml
    f_result = open(result_xml, 'w')
    f_result.writelines(lines)
    f_result.close()


def local_test(img_file=TEST_IMG, predic_path=PREDICTOR_MODEL):
    """
    Use predict_model to detect face in img, and show the result in a window.
    Default values for parameters can be changed.

    :param img: A jpg image that contains a face.
    :param predict_model: The model for predicting face.
    :return: None
    """
    # print(PARENT_PATH)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(PREDICTOR_MODEL)
    img = io.imread(img_file)

    win = dlib.image_window()
    win.clear_overlay()
    win.set_image(img)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)

    print("Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        # Get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        # Draw the face landmarks on the screen.
        win.add_overlay(shape)

    win.add_overlay(dets)
    dlib.hit_enter_to_continue()


if __name__ == '__main__':
    num_args = len(sys.argv)
    if num_args == 1:
        local_test()
    elif num_args == 2:
        local_test(sys.argv[1])
    elif num_args == 3:
        local_test(sys.argv[1], sys.argv[2])
    else:
        print(
            "Usage:\n"
            "\n\t1: python local_test.py"
            " (Use default image and default predictor model)"
            "\n\t2: python local_test.py <img>"
            " (Use specified image and default predictor model)"
            "\n\t3: python local_test.py <img> <predictor-model>"
            " (Use specified image and specified predictor model)")
        exit()
