import itertools
import hashlib

import numpy as np

from PIL import Image

__all__ = ['find_modified']


def load_image(infilename):
    """
    Load image as a np array
    :param infilename: file path to the image
    :return: image np array
    """
    img = Image.open(infilename)
    data = np.asarray(img, dtype="int32")
    return data


def filter_images(images):
    """
    Check if all images have 3 channels
    :param images: list of paths to the images
    :return: image list with only 3 channels images
    """
    image_list = []
    # count_all = len(images)
    for c, image in enumerate(images):
        # print('Checking image #' + str(c + 1) + ' out of ' + str(count_all))
        try:
            assert load_image(image).shape[2] == 3
            image_list.append(image)
        except AssertionError as e:
            print(e)
    return image_list


def img_gray(image):
    """
    turning image into greyscale
    :param image: image path
    :return: loaded image in greyscale as np array
    """
    image = Image.open(image)
    return np.average(image, weights=[0.2989, 0.5870, 0.1140], axis=2)


def resize(image, height=30, width=30):
    """
    resize image, first load it from np array, then resize it with
    cubic interpolation and convert again in flatten np array
    :param image: image as np array
    :param height: image new height
    :param width: image new width
    :return: tuple of np array rows and cols for resize image
    """
    image = Image.fromarray(image)
    row_res = image.resize((width, height), Image.CUBIC)
    row_res = np.asarray(row_res, dtype="int32").flatten()
    col_res = image.resize((width, height), Image.CUBIC)
    col_res = np.asarray(col_res, dtype='int32').flatten('F')
    return row_res, col_res


def intensity_diff(row_res, col_res):
    """
    gradient direction (finding changes) based on intensity
    :param row_res: np array of image rows
    :param col_res: np array of image cols
    :return:
    """
    difference_row = np.diff(row_res)
    difference_col = np.diff(col_res)
    difference_row = difference_row > 0
    difference_col = difference_col > 0
    return np.vstack((difference_row, difference_col)).flatten()


def file_hash(array):
    """
    convert image as array to hash using sha256
    :param array: image as array
    :return: hash of this array
    """
    return hashlib.sha256(array).hexdigest()


def difference_score(image, height=30, width=30):
    """
    getting something like image 'blueprint' from image or custom hash for image
    :param image: image path
    :param height: height of 'blueprint'
    :param width: width of 'blueprint'
    :return: image 'blueprint'
    """
    gray = img_gray(image)
    row_res, col_res = resize(gray, height, width)
    difference = intensity_diff(row_res, col_res)

    return difference


def difference_score_dict_hash(image_list):
    """
    calculating totally duplicate images using sha256 hash function
    :param image_list: paths to images
    :return: paths to duplicate images as a list of tuple where
    in one tuple will be duplicates
    """
    ds_dict = {}
    duplicates = []
    hash_ds = []
    for image in image_list:
        ds = difference_score(image)
        hash_ds.append(ds)
        filehash = file_hash(ds)
        if filehash not in ds_dict:
            ds_dict[filehash] = image
        else:
            duplicates.append((image, ds_dict[filehash]))

    return duplicates


def hamming_distance(image, image2):
    """
    calculating hamming distance between images represented as 1-D arrays
    :param image: first image
    :param image2: second image
    :return: hamming distance
    """
    score = np.count_nonzero(image != image2)
    return score / len(image)


def difference_score_dict(image_list):
    """
    calculating duplicate and modified images using hamming distance
    :param image_list: paths to filtered images
    :return: paths to duplicate and modified images as a list of tuple
    where in one tuple will be duplicates and modified
    """
    ds_dict = {}
    duplicates = []
    # count_all = len(image_list)
    for c, image in enumerate(image_list):
        # print('Processing image #' + str(c + 1) + ' out of ' + str(count_all))
        ds = difference_score(image)

        if image not in ds_dict:
            ds_dict[image] = ds
        else:
            duplicates.append((image, ds_dict[image]))

    return duplicates, ds_dict


def find_modified(all_files):
    """
    finding modified images
    :param all_files: list of paths to all images
    :return: path to duplicate and modified images
    """
    # print('Checking images shapes...')
    image_files = filter_images(
        all_files)  # filtering images due to 3 channels shape cause we will turn them in greyscale

    # print('Finding similar with Hamming distance')
    modified, ds_dict = difference_score_dict(image_files)

    for k1, k2 in itertools.combinations(ds_dict, 2):
        if hamming_distance(ds_dict[k1], ds_dict[k2]) < .10:
            modified.append((k1, k2))
    return modified
