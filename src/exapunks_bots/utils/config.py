from __future__ import annotations

import logging
from configparser import ConfigParser as _ConfigParser

from . import utils

_logger = logging.getLogger(__name__)


class Config(object):
    def __init__(self, config_path, section: str | list = '', **kwargs):
        _logger.info(f"Loading config file '{config_path}'")

        # Set given global attributes
        setattr(self, "CONFIG_PATH", config_path)
        for key, value in kwargs.items():
            setattr(self, key.upper(), value)

        exist = utils.existPath(config_path)
        if not exist:
            path_, exist = utils.checkPath(kwargs.get('root_dir'), utils.getLastPath(config_path), errors='warn')
            if not exist:
                return
            config_path = path_

        config_ = {}
        if exist:
            parser = _ConfigParser()
            parser.optionxform = str
            parser.read(config_path)

            if section and isinstance(section, str):
                # Get section attributes from config file
                if parser.has_section(section):
                    config_ = {key: eval(value) for key, value in parser.items(section)}
                    setattr(self, "SECTION", section)
                else:
                    _logger.error(f"Section '{section}' not found in '{config_path}'")
            elif section and isinstance(section, list):
                # Get specific sections attributes from config file
                for section_ in section:
                    if parser.has_section(section_):
                        config_ = {key: eval(value) for key, value in parser.items(section_)}
                        if hasattr(self, "SECTIONS"):
                            self.SECTIONS.extend(section_)
                        else:
                            setattr(self, "SECTIONS", [section_])
                    else:
                        _logger.error(f"Section '{section_}' not found in '{config_path}'")
            else:
                # Get all attributes from config file
                for each_section in parser.sections():
                    config_[each_section] = {key: eval(value) for key, value in parser.items(each_section)}

        # Set found config attributes
        for key in config_:
            setattr(self, key, config_.get(key, False))

    def __str__(self):
        return str(self.__dict__)
