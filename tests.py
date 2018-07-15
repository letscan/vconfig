# coding: utf-8
from vconfig import VConfig

V = VConfig(__file__)

assert V.BASE_URL == 'https://github.com/letscan', V.BASE_URL
