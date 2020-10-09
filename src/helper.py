from os import listdir
import pandas as pd
import logging
import pickle


def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def read_csv(path_to_dir, name):
    # TODO check if the path exist
    return pd.read_csv(path_to_dir+name)


def create_logger(name, logFile, fileLogLevel, streamLogLevel):
    # create logger for "Sample App"
    logger = logging.getLogger(name)
    logger.setLevel(logging.NOTSET)

    # create file handler which logs WARNING messages
    fh = logging.FileHandler(logFile, mode='w')
    fh.setLevel(fileLogLevel)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(streamLogLevel)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] %(levelname)8s --- %(message)s ' +
                                  '(%(filename)s:%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


def dump_file(location, file):
    try:
        with open(location, 'wb') as f:
            pickle.dump(file, f)
    except:
        print("Error in dumping File")


def load_file(location):
    try:
        with open(location, 'rb') as f:
            return pickle.load(f), True
    except:
        return None, False
