from os import listdir
import pandas as pd
import logging
import pickle


def find_csv_filenames(path_to_dir, suffix=".csv"):
    """Find Names of CSV files

    Args:
        path_to_dir (string): Path to the directory
        suffix (str, optional): Extension to use. Defaults to ".csv".

    Returns:
        List of file Names.
    """
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def read_csv(path_to_dir, name) -> pd.DataFrame:
    """Function to read a CSV File.

    Args:
        path_to_dir (str): Location of directory.
        name (str): Name of file.

    Returns:
        pd.DataFrame
    """
    # TODO : check if the path exist
    return pd.read_csv(path_to_dir+name)


def create_logger(name: str, logFile: str, fileLogLevel, streamLogLevel):
    """It will create a logger object.

    Args:
        name (str): Name of Logger
        logFile (str): Location to store the logger
        fileLogLevel : Logger object
        streamLogLevel: Logger object

    Returns:
        Logger
    """
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


def dump_file(location: str, file) -> None:
    """Dumps a pickle file to a desired location.

    Args:
        location (str): Name of Location.
        file : File to save as pkl.
    """
    try:
        with open(location, 'wb') as f:
            pickle.dump(file, f)
    except:
        print("Error in dumping File")


def load_file(location):
    """Loads a pickle file from a desired location.

    Args:
        location (str): Name of Location.

    Returns:
        File -> None if file not found
        Flag -> Error Happened/File not found.

    """
    try:
        with open(location, 'rb') as f:
            return pickle.load(f), True
    except:
        return None, False
