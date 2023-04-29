from __future__ import annotations

import inspect
import json
import logging
import os
import pickle
import re
from typing import Any

_logger = logging.getLogger(__name__)


def camelToSnake(value: str) -> str:
    """Convert CamelCase to snake_case"""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', value).lower()


def checkPath(path: str, *paths, ext: str = '', errors: str = 'ignore', return_exist: bool = True) -> tuple | str:
    """
    Join the paths together, adds an extension if not already included
    in path, then checks if path exists.

    :param path: Main file path, should be a str
    :param paths: Remaining file paths, should be a tuple[str]
    :param ext: File extension, should be a str
    :param errors: Whether to 'ignore', 'warn' or 'raise' errors, should be str
    :param return_exist: Whether to return the status of the path, should be a bool
    :return: path, exist - tuple[str, bool] | str
    """
    if errors not in ["ignore", "warn", "raise"]:
        raise ValueError("The parameter errors must be either 'ignore', 'warn' or 'raise'")

    path = joinPath(path, *paths, ext=ext)

    exist = True if os.path.exists(path) else False

    if not exist:
        msg = f"No such file or directory: '{path}'"
        _logger.debug(msg)
        if errors == 'warn':
            _logger.warning(msg)
        elif errors == 'raise':
            raise FileNotFoundError(msg)
    if not return_exist:
        return path
    return path, exist


def existPath(path: str, *paths, ext: str = '', errors: str = 'ignore') -> bool:
    """
    Join the paths together, adds an extension if not already included
    in path, then checks if path exists.

    :param path: Main file path, should be a str
    :param paths: Remaining file paths, should be a tuple[str]
    :param ext: File extension, should be a str
    :param errors: Whether to 'ignore', 'warn' or 'raise' errors, should be str
    :return: exist - bool
    """
    _, exist = checkPath(path, *paths, ext=ext, errors=errors)
    return exist


def joinPath(path: str, *paths, ext: str = '') -> str:
    """
    Join the paths together, adds an extension if not already included
    in path.

    :param path: Main file path, should be a str
    :param paths: Remaining file paths, should be a tuple[str]
    :param ext: File extension, should be a str
    :return: path - str
    """
    path, path_ext = os.path.splitext(os.path.join(path, *filter(lambda x: x and isinstance(x, str), paths)))
    if ext and path_ext != ext:
        path_ext = (ext if ext and '.' in ext else f'.{ext}')
    return path + path_ext


def makePath(path: str, *paths, errors: str = 'ignore') -> str:
    """
    Check if the path exists and creates the path when required.

    :param path: Main file path, should be a str
    :param paths: Remaining file paths, should be a tuple[str]
    :param errors: Whether to 'ignore', 'warn' or 'raise' errors, should be str
    :return: path - str
    """
    path, exist = checkPath(path, *paths, errors=errors)
    if not exist:
        os.makedirs(path)
        _logger.debug(f"Path has been made: '{path}'")
    return path


def listPath(path: str, *paths, ext: str | list | tuple = None, return_file_path: bool = False,
             errors: str = 'ignore') -> tuple:
    """
    Join the paths together, return list of files within directory or
    specific files by extension.

    :param path: Main file path, should be a str
    :param paths: Remaining file paths, should be a tuple[str]
    :param ext: File extension, should be a str | list | tuple
    :param return_file_path: Whether to return file name or file path, should be a bool
    :param errors: Whether to 'ignore', 'warn' or 'raise' errors, should be str
    :return: path, files - tuple[str, list[str]]
    """
    if errors not in ["ignore", "warn", "raise"]:
        raise ValueError("The parameter errors must be either 'ignore', 'warn' or 'raise'")

    if not ext:
        ext = []
    elif isinstance(ext, str):
        ext = [ext]
    elif not isinstance(ext, (list, tuple)):
        raise TypeError(f"'ext': Expected type 'str', 'list' or 'tuple', got: '{type(ext).__name__}'")

    ext = [_.replace('.', '') for _ in ext]

    files = []
    path, exist = checkPath(path, *paths, errors=errors)
    if not exist:
        return path, files

    for file in os.listdir(path):
        file_ext = os.path.splitext(file)[1].replace('.', '')
        if not ext or file_ext in ext:
            files.append(joinPath(path, file) if return_file_path else file)
    return path, files


def splitPath(path: str, direction: str = 'lr', max_split: int = 1, include_ext: bool = True) -> tuple:
    """
    Splits the path into left and right by direction with split size.

    :param path: Path to a folder or file, should be a str
    :param direction: Whether to split the path from 'lr' or 'rl', should be str
    :param max_split: The splitting size, should be an int
    :param include_ext: Whether to include file extension, should be a bool
    :return: left, right - tuple[str, str]
    """
    sep_path = re.split("\\\\|/", path)
    if max_split not in range(1, len(sep_path)):
        raise ValueError(f"'max_split' must be within range of 1 and directory depth, got: {max_split}")

    if direction == 'lr':
        left, right = sep_path[:max_split], sep_path[max_split:]
    elif direction == 'rl':
        left, right = sep_path[:(len(sep_path) - max_split)], sep_path[(len(sep_path) - max_split):]
    else:
        raise ValueError("The parameter direction must be either 'lr' or 'rl'")

    if not include_ext:  # removes the file extension
        right[-1] = os.path.splitext(right[-1])[0]
    return os.sep.join(left), os.sep.join(right)


def getLastPath(path: str, include_ext: bool = True) -> str:
    """
    Splits the last path from the given path and includes the option
    to remove file extension.

    :param path: Path to a folder or file, should be a str
    :param include_ext: Whether to include file extension, should be a bool
    :return: last_path - str
    """
    return splitPath(path, direction='rl', max_split=1, include_ext=include_ext)[1]


def getRelativePath(*paths, ext: str = ''):
    """
    Gets the relative path of the callback location

    :param paths: Remaining file paths, should be a tuple[str]
    :param ext: File extension, should be a str
    :return: path - str
    """
    callback_path = inspect.stack()[1].filename
    relative_path = ''
    if os.name == 'nt':
        relative_path = splitPath(callback_path, direction='rl', max_split=1)[0]
    elif os.name == 'posix':
        relative_path = splitPath(callback_path, direction='lr', max_split=1)[0]
    return joinPath(relative_path, *paths, ext=ext)


def addEnvPath(*paths, env_name: str = 'PATH', path_sep: str = ',', errors: str = 'raise') -> None:
    """
    Add paths to environment paths.

    :param paths: Remaining file paths, should be a tuple[str]
    :param env_name: Name of environment path to be added, should be a str
    :param path_sep: Seperator the can split joined str paths, should be a str
    :param errors: Whether to 'ignore', 'warn' or 'raise' errors, should be str
    :return: - None
    """
    if len(paths) == 1:
        if isinstance(paths[0], (list, tuple)):
            paths = paths[0]
        elif isinstance(paths[0], str):
            paths = paths[0].split(path_sep)

    for env_path in paths:
        if env_path and existPath(env_path, errors=errors):
            existing_paths = list(filter(bool, [os.environ.get(env_name)]))
            existing_paths.append(env_path)
            os.environ[env_name] = ';'.join(existing_paths)


def condense(array: list | tuple) -> list:
    """
    Uses recursion to condense a multidimensional array into a 1D flattened
    array.

    :param array: Array to be condensed, should be a list[Any] | tuple[Any]
    :return: condensed_array - list[Any]
    """
    condensed_array = []
    for item in array:
        if isinstance(item, (list, tuple)):
            condensed_array += condense(item)
        else:
            condensed_array.append(item)
    return condensed_array


def getDictKeys(array: dict, dict_keys: list = None) -> list:
    """
    Uses recursion to find all keys within dictionary and sub dictionaries.

    :param array: Dictionary of keys and values, should be a dict[str| Any: Any]
    :param dict_keys: List of keys used in given array, should be a dict
    :return: dict_keys - list[str | Any]
    """
    if dict_keys is None:
        dict_keys = []

    for key, item in list(array.items()):
        if isinstance(item, dict):
            dict_keys = getDictKeys(item, dict_keys)
        dict_keys.append(key)
    return dict_keys


def update(obj: object, kwargs: dict, errors='ignore') -> object:
    """
    Update the objects attributes, if given attributes are present
    in object and match existing data types.

    :param obj: The object that is being updated, should be an object
    :param kwargs: Keywords and values to be updated, should be a dict
    :param errors: Whether to 'ignore', 'warn' or 'raise' errors, should be str
    :return: obj - object
    """
    if errors not in ["ignore", "warn", "raise"]:
        raise ValueError("The parameter errors must be either 'ignore', 'warn' or 'raise'")

    kwargs = dict(zip(map(camelToSnake, list(kwargs.keys())), list(kwargs.values())))

    for key, value in kwargs.items():
        if not hasattr(obj, key):
            msg = f"'{obj.__class__.__name__}' object has no attribute '{key}'"
            _logger.debug(msg)
            if errors == 'warn':
                _logger.warning(msg)
            elif errors == 'raise':
                raise AttributeError(msg)
            continue
        attr_ = getattr(obj, key)
        if isinstance(value, type(attr_)) or (type(attr_).__name__ == type(value).__name__):
            setattr(obj, key, value)
            continue

        msg = f"'{key}': Expected type '{type(attr_).__name__}', got '{type(value).__name__}'"
        _logger.debug(msg)
        if errors == 'warn':
            _logger.warning(msg)
        elif errors == 'raise':
            raise TypeError(msg)
    return obj


def toJson(obj: object, errors='raise') -> Any:
    """
    Serializer method will return the JSON representation of the object.

    :param obj: Object to be serialized, should be an object
    :param errors: Whether to 'ignore', 'warn' or 'raise' errors, should be str
    :return:
    """
    if errors not in ["ignore", "warn", "raise"]:
        raise ValueError("The parameter errors must be either 'ignore', 'warn' or 'raise'")

    if hasattr(obj, 'toJson'):
        if callable(obj.toJson):
            return obj.toJson()

        msg = f"'{obj.__name__}': Expected type 'Callable', got '{type(obj.toJson).__name__}'"
        _logger.debug(msg)
        if errors == 'warn':
            _logger.warning(msg)
        elif errors == 'raise':
            raise TypeError(msg)
    else:
        if isinstance(obj, set):
            return list(obj)

        msg = f"'{obj.__name__}' object has no attribute 'toJson'"
        _logger.debug(msg)
        if errors == 'warn':
            _logger.warning(msg)
        elif errors == 'raise':
            raise AttributeError(msg)
    return None


def load(dir_: str, name: str, ext: str = '', errors: str = 'raise') -> Any:
    """
    Load the data with appropriate method. Pickle will deserialise the
    contents of the file and json will load the contents.

    :param dir_: Directory of file, should be a str
    :param name: Name of file, should be a str
    :param ext: File extension, should be a str
    :param errors: Whether to 'ignore', 'warn' or 'raise' errors, should be str
    :return: data - Any
    """
    if errors not in ["ignore", "warn", "raise"]:
        raise ValueError("The parameter errors must be either 'ignore', 'warn' or 'raise'")

    if not ext:
        ext = os.path.splitext(name)[1]

    if not ext:
        msg = f"The parameters 'name' or 'ext' must include file extension, got: '{name}', '{ext}'"
        _logger.debug(msg)
        if errors == 'warn':
            _logger.warning(msg)
        elif errors == 'raise':
            raise ValueError(msg)
        return

    path, exist = checkPath(dir_, name, ext=ext, errors=errors)

    if not exist:
        return None

    if ext == '.json':
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    elif ext == '.txt':
        with open(path, 'r') as file:
            data = file.read()
    else:
        with open(path, 'rb') as file:
            data = pickle.load(file)
    _logger.debug(f"File '{name}' data was loaded")
    return data


def save(dir_: str, name: str, data: Any, indent: int = 4, errors: str = 'raise') -> bool:
    """
    Save the data with appropriate method. Pickle will serialise the
    object, while json will dump the data with indenting to allow users
    to edit and easily view the encoded data.

    :param dir_: Directory of file, should be a str
    :param name: Name of file, should be a str
    :param data: Data to be saved, should be an Any
    :param indent: Data's indentation within the file, should be an int
    :param errors: If 'ignore', suppress errors, should be str
    :return: completed - bool
    """
    if errors not in ["ignore", "warn", "raise"]:
        raise ValueError("The parameter errors must be either 'ignore', 'warn' or 'raise'")

    path = joinPath(dir_, name)
    ext = os.path.splitext(name)[1]

    if not existPath(dir_, errors=errors):
        return False

    if not ext:
        msg = f"File '{name}' must include file extension in name"
        _logger.debug(msg)
        if errors == 'warn':
            _logger.warning(msg)
        elif errors == 'raise':
            raise ValueError(msg)
        return False

    if ext == '.json':
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, default=toJson, indent=indent)
    elif ext == '.txt':
        with open(path, 'w') as file:
            file.write(str(data))
    elif isinstance(data, object):
        with open(path, 'wb') as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
    else:
        msg = f"Saving method was not determined, failed to save file, got: {type(data)}"
        _logger.debug(msg)
        if errors == 'warn':
            _logger.warning(msg)
        elif errors == 'raise':
            raise FileNotFoundError(msg)
        return False
    _logger.debug(f"File '{name}' was saved")
    return True
