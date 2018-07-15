# coding: utf-8
"""Easy to use configuration module
"""
import json
import os
import time


class VConfig(object):
    """Easy to use configuration module

    >>> from vconfig import VConfig
    >>> V = VConfig(__file__)
    >>> print(V.BASE_URL)
    """
    config_name = 'vconfig.json'
    expire_seconds = 30

    def __init__(self, path):
        self.config_files = []
        self.find_configs(path)
        self.config = {}
        self._update_at = 0

    def __getattr__(self, name):
        if time.time() - self._update_at > self.expire_seconds:
            self.load_configs()
        try:
            return self.config[name]
        except KeyError:
            raise AttributeError('No such config: {}'.format(name))

    def find_configs(self, path):
        path = os.path.realpath(path)
        if os.path.isfile(path):
            dirpath = os.path.dirname(path)
        elif os.path.isdir(path):
            dirpath = path
        else:
            raise IOError('File not found: {}'.format(path))
        config_path = os.path.join(dirpath, self.config_name)
        while not os.path.isfile(config_path):
            dirpath = os.path.dirname(dirpath)
            config_path = os.path.join(dirpath, self.config_name)
        while os.path.isfile(config_path):
            self.config_files.append(config_path)
            dirpath = os.path.dirname(dirpath)
            config_path = os.path.join(dirpath, self.config_name)

    def load_configs(self):
        for config_file in reversed(self.config_files):
            with open(config_file) as fp:
                self.config.update(json.load(fp))
        self._update_at = time.time()
