#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 - 2019 Syrian Programmer.
#
# Slack Bot
#

from slackclient import SlackClient
import websocket
from config import config
import log_event
import functions_commands

from threading import Thread
import queue
import time
import re

# config to set path log and set handler file, stream.
PATH_LOG = config.conf_logging['PATH_FILE_LOG']
logger = log_event.Logging(PATH_LOG)
logger.level_name = __name__
logger.file_handler = config.conf_logging['HANDLER_FILE']
logger.stream_handler = config.conf_logging['HANDLER_STREAM']
logger.info('Loading all library successful :)')

# n second delay between reading from real time read
REAL_TIME_READ_DELAY = config.conf_settings['REAL_TIME_READ_DELAY']


class SlackBot:
    """
    The Slack Bot makes API Calls
    """

    def __init__(self):
        # initialize api token
        self.slack_client = SlackClient(config.conf_settings['API_TOKEN'])

        self.__queue = queue.Queue()

        thread_listener = Thread(target=self.__listener_real_time)
        thread_listener.start()

        self._process_event()

    def __listener_real_time(self):
        """
        thread to received all events and put in queue
        :return:
        """
        if not self.slack_client.rtm_connect(with_team_state=False, auto_reconnect=True):
            logger.error('func: __listener_real_time, err: Connection failed.')
            return

        logger.info('func: __listener_real_time, msg: Slack Bot connected and running!.')
        while True:
            try:
                received_message = self.slack_client.rtm_read()
                if received_message:
                    self.__queue.put(received_message)
                time.sleep(REAL_TIME_READ_DELAY)

            except websocket.WebSocketConnectionClosedException as err:
                logger.error('func: __listener_real_time err: {}'.format(err))
                logger.error('Caught websocket disconnect, reconnecting...')
                time.sleep(REAL_TIME_READ_DELAY)
                self.slack_client.rtm_connect(with_team_state=False, auto_reconnect=True)

            except Exception as err:
                logger.error('func: __listener_real_time err: {}'.format(err))
                time.sleep(REAL_TIME_READ_DELAY)

    def _process_event(self):
        """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
        :return:
        """
        while True:

            if self.__queue.empty():
                time.sleep(0.5)
                continue

            # get events from queue.
            slack_events = self.__queue.get()

            # get command and channel from event.
            command, channel = self.parse_bot_commands(slack_events)

            if not command:
                continue

            # run command as thread.
            try:
                Thread(target=self.handel_commands, args=(command, channel)).start()
            except Exception as err:
                logger.error('func: _process_event, error: {}'.format(err))
                logger.error('thread: handel_commands, args: command {}, channel {}'.format(command, channel))

    def parse_bot_commands(self, slack_events):
        """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
        :param slack_events:
        :return: tuple of command, channel or None, None.
        """
        for event in slack_events:
            if 'type' in event and event['type'] == 'message' and 'subtype' not in event:
                # extract command and user_id from message
                user_id, message = self.parser_direct_mention(event['text'])
                if message:
                    return message, event["channel"]
        return None, None

    @staticmethod
    def parser_direct_mention(message_text: str):
        """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
        :param message_text: EX: '<@UC89AFJSC> hallo'
        :return:
        """
        matches = re.search("^<@(|[WU].+?)>(.*)", message_text)
        if not matches:
            return None, None

        # the first group contains the username, the second group contains the remaining message
        return matches.group(1), matches.group(2).strip()

    @staticmethod
    def handel_commands(command: str, channel: str):
        """
        Executes bot command if the command is known
        :param command:
        :param channel:
        :return:
        """

        if command.startswith('/shell'):
            functions_commands.command_shell(command, channel)


if __name__ == "__main__":
    SlackBot()
