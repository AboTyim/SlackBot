#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 - 2019 Syrian Programmer.
#
# module for config project
# Settings file using for save program options by default.
#

import os

# Get local path file config only folder
path_local = os.path.dirname(os.path.abspath(__file__))

# Get local path workspace
path_workspace = os.path.dirname(path_local)

conf_settings = {
    'API_TOKEN': 'xoxb-XXXXXXXXX-XXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXX',

    'ID_BOT_ARCHIVE_TWITTER': 'XXXXXXXX',
    'ID_CHANNEL_ARCHIVE': 'XXXXXXXX',

    'REAL_TIME_READ_DELAY': 1,

    'ERROR_COMMAND': 'تأكد من كتابة الأمر بالشكل الصحيح',

}
conf_logging = {
    'PATH_FILE_LOG': os.path.join(path_workspace, 'info', 'logging.log'),
    'HANDLER_FILE': 'DEBUG',
    'HANDLER_STREAM': 'ERROR',
}
