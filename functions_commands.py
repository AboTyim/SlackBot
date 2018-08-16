#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 - 2019 Syrian Programmer.
#
# module functions commands such as send message, archive, watcher, etc...
#

from slackclient import SlackClient
from config import config
import log_event
import subprocess

# config to set path log and set handler file, stream.
PATH_LOG = config.conf_logging['PATH_FILE_LOG']
logger = log_event.Logging(PATH_LOG)
logger.level_name = __name__
logger.file_handler = config.conf_logging['HANDLER_FILE']
logger.stream_handler = config.conf_logging['HANDLER_STREAM']

# instantiate Slack client
_slack_client = SlackClient(config.conf_settings['API_TOKEN'])

# n second delay between reading from real time read
REAL_TIME_READ_DELAY = config.conf_settings['REAL_TIME_READ_DELAY']


def send_message(channel: str, message: str):
    """
    Sends the response back to the channel.
    :param channel: name channel to send message.
    :param message: text message
    :return:
    """
    _slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        as_user=True
    )


def command_shell(message: str, channel: str):
    """
    Command to execute command shell on server.
    :param message: command as text
    :param channel:id channel to send notification
    :return:
    """
    if len(message.split()) < 2:
        send_message(channel, config.conf_settings['ERROR_COMMAND'])
        return

    cmd = message
    # remove /shell from command
    command = cmd[6::]
    # execute command shell
    output = subprocess.getoutput(command)
    # send result output command to user
    send_message(channel, output)
