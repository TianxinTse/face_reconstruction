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
    :return: landmarks
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
