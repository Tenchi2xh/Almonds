# -*- encoding: utf-8 -*-

import time
import datetime


class Logger:
    def __init__(self):
        self.log = []

    def __call__(self, message):
        ts = datetime.datetime.fromtimestamp(time.time()).strftime("(%H:%M) ")
        self.log.append(ts + str(message))

    def __getitem__(self, item):
        self.log.__getitem__(item)

    def get_latest(self, n):
        return self.log[-n:][::-1]