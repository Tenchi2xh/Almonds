# -*- encoding: utf-8 -*-

import time
import datetime


class Logger(object):
    """
    Simple logger class.

    Stores all logging messages in an list after prepending a timestamp.
    """
    def __init__(self):
        """
        Initializes the log list.
        """
        self.log = []

    def __call__(self, message):
        """
        Apply method to use an instance object as a function to log messages.

        >>> log = Logger()
        >>> log("Hello, World!")

        :param message: Message to log
        :return:
        """
        ts = datetime.datetime.fromtimestamp(time.time()).strftime("(%H:%M) ")
        self.log.append(ts + str(message))

    def __getitem__(self, index):
        """
        Accessor function to retrieve a log by its index.

        >>> log = Logger()
        >>> ...
        >>> print log[0]
        "Hello, World!"

        :param index: Index of desired message.
        :return: Desired message.
        """
        return self.log.__getitem__(index)

    def get_latest(self, n):
        """
        Retrieves the `n` latest messages from the log.

        :param n: Number of messages to retrieve.
        :return: `n` latest messages.
        """
        return self.log[-n:][::-1]
