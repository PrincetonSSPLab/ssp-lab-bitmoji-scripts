#!/usr/bin/env python

"""Command line tool that offers functionality to split of directories of
flies into individual batches.
"""

import argparse
import os
import random
import shutil


def gather_filenames(directory_path):
    """Gathers all the images from a directory and returns a list of
    the filenames.

    Parameters
    ----------
    directory_path: str
        The path to the directory containing all the images.

    Returns
    -------
    List:
        List of absolute filepath to images.

    """
    filenames = os.listdir(directory_path)
    abs_filepaths = []
    for filename in filenames:
        full_filepath = os.path.join(directory_path, filename)
        absolute_filepath = os.path.abspath(full_filepath)
        abs_filepaths.append(absolute_filepath)

    return abs_filepaths


def split_filepaths_into_batches(all_image_paths, batch_size,
                                 shuffle=True, seed=None):
    """Takes in a list of filepaths, randomizes their order, then creates a
    dictionary where the key is the number of the batch and the value is a
    list of filepaths.

    Parameters
    ----------
    seed: int
        Seed for the random number generator.

    all_image_paths: List of Str
        List of filepaths.

    batch_size: int
        How big batches should be.

    shuffle: bool
        Whether to shuffle the list of filepaths.

    Returns
    -------
    Dict:
        Dictionary where they key is an int of batch number and value is a
        list of filepaths.
    """
    if seed is not None:
        random.seed(seed)
    if shuffle:
        random.shuffle(all_image_paths)
    batches = {}
    for j, i in enumerate(range(0, len(all_image_paths), batch_size), 1):
        batches[j] = all_image_paths[i:i + batch_size]

    return batches


def create_batch_folder(list_of_filepaths, folder_name, directory):
    """Takes a batch of images in list format, creates a folder for all the
    images in the batch, and copies the images to the new folder.

    Parameters
    ----------
    list_of_filepaths: list
        Stings of file paths.

    folder_name: str
        Name of the batch folder that will be made.

    directory: str
        Location where the batch folder will be created.
    """
    folder_path = os.path.join(directory, folder_name)
    if os.path.exists(folder_path):
        os.rmdir(folder_path)
    os.makedirs(folder_path)

    for filepath in list_of_filepaths:
        shutil.copy(filepath, folder_path)


def create_all_batches(batches_dict, directory):
    """Creates all the individual batches form the dictionary of batches.

    Parameters
    ----------
    batches_dict: dict
        Dictionary where they key is an int of batch number and value is a
        list of filepaths.

    directory: str
        Parent directory where all the batch folders will be made.
    """
    for batch_no, files in batches_dict.items():
        folder_name = "Batch " + str(batch_no)
        create_batch_folder(files, folder_name, directory)


def initialize_parser():
    """Initializes the parser for the command line arguments.

    Returns
    -------
    parser: ArgumentParser
        Parser for the command line arguments.
    """
    parser = argparse.ArgumentParser(description="Command line tool that "
                                                 "offers functionality to "
                                                 "split of directories of "
                                                 "flies into individual "
                                                 "batches.")
    parser.add_argument("-d", "--directory", help="Directory containing all "
                                                  "the images.",
                        required=True)
    parser.add_argument("-b", "--batch_size", help="Size of the batches.",
                        required=False, default=100)
    parser.add_argument("-s", "--shuffle", help="Whether or not to shuffle "
                                                "the images.",
                        required=False, default=True)
    parser.add_argument("-o", "--output_directory", help="Directory where "
                                                         "the batches will "
                                                         "be created.",
                        required=False, default=os.getcwd())
    parser.add_argument("-S", "--seed", help="Seed for the random number "
                                             "generator.",
                        required=False, default=None)

    return parser


def main():
    """Main function for the command line tool."""
    parser = initialize_parser()
    args = parser.parse_args()
    directory = args.directory
    batch_size = args.batch_size
    shuffle = args.shuffle
    output_directory = args.output_directory

    all_image_paths = gather_filenames(directory)
    batches_dict = split_filepaths_into_batches(all_image_paths, batch_size,
                                                shuffle)
    create_all_batches(batches_dict, output_directory)


if __name__ == '__main__':
    main()
