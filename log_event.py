#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Library to logging.
#
#
# Copyright (c) 2018 - 2019 Syrian Programmer.
#
#
# __author__ = 'Syrian Programmer'
# __nickname__ = 'Abu Tyim Technical'
# __version__ = '0.1'

import logging


class Logging:
    def __init__(self, path, level_fh='DEBUG', level_sh='ERROR'):
        self.__name = 'root'
        self.__level_FileHandler = level_fh
        self.__level_StreamHandler = level_sh
        self.__path = path
        self.__format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'

        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(self.__level_FileHandler)

        # create file handler which logs even debug messages
        fh = logging.FileHandler(self.__path)
        fh.setLevel(self.__level_FileHandler)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(self.__level_StreamHandler)

        # create formatter and add it to the handlers
        formatter = logging.Formatter(self.__format)
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add the handlers to logger
        self.__logger.addHandler(ch)
        self.__logger.addHandler(fh)

    ####################################

    def __update_file_handler(self):
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(self.__level_FileHandler)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(self.__path)
        fh.setLevel(self.__level_FileHandler)

        formatter = logging.Formatter(self.__format)
        fh.setFormatter(formatter)
        fh.setLevel(self.__level_FileHandler)
        self.__logger.addHandler(fh)

    def __update_stream_handler(self):
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(self.__level_FileHandler)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(self.__level_StreamHandler)

        # create formatter and add it to the handlers
        formatter = logging.Formatter(self.__format)
        ch.setFormatter(formatter)

        # add the handlers to logger
        self.__logger.addHandler(ch)

    @property
    def level_name(self):
        return self.__name

    @level_name.setter
    def level_name(self, log_name):
        self.__name = log_name
        # self.__update_file_handler()
        # self.__update_stream_handler()

    ####################################

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path_log):
        self.__path = path_log

    ####################################

    @property
    def format(self):
        return self.__format

    @format.setter
    def format(self, fmt):
        self.__format = fmt

    ####################################

    @property
    def file_handler(self):
        return self.__level_FileHandler

    @file_handler.setter
    def file_handler(self, level):
        self.__level_FileHandler = level
        self.__update_file_handler()

    ####################################

    @property
    def stream_handler(self):
        return self.__level_StreamHandler

    @stream_handler.setter
    def stream_handler(self, level):
        self.__level_StreamHandler = level
        self.__update_stream_handler()

    ####################################

    def info(self, msg):
        self.__logger.info(msg)

    def debug(self, msg):
        self.__logger.debug(msg)

    def critical(self, msg):
        self.__logger.critical(msg)

    def error(self, msg):
        self.__logger.error(msg)

    def warning(self, msg):
        self.__logger.warning(msg)

    def warn(self, msg):
        self.__logger.warn(msg)


if __name__ == '__main__':
    logger = Logging('/home/conan/file.log')
    logger.path = '/home/conan/file.log'
    logger.level_name = 'My app Test'
    logger.file_handler = 'DEBUG'
    logger.stream_handler = 'ERROR'

    logger.debug('Stating debug My app Test')
    logger.info('Stating info My app Test')
    logger.error('Stating error My app Test')
    logger.warning('Stating warning My app Test')
    logger.critical('Stating critical My app Test')

    logger.level_name = 'main'
    logger.file_handler = 'INFO'
    logger.stream_handler = 'ERROR'

    logger.debug('Stating debug main')
    logger.info('Stating info main')
    logger.error('Stating error main')
    logger.warning('Stating warning main')
    logger.critical('Stating critical main')
