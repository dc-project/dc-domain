#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: ex_domain/tools.py 
@time: 2017/11/6 17:08
"""

import string
import random


def make_wild_name():
    all_chars = string.ascii_lowercase + string.digits
    ss = list(random.choice(all_chars) for _ in range(4))
    ss.insert(3, random.choice(string.ascii_lowercase))
    return ''.join(ss)


def is_passive_wild_name(ss):
    return bool(ss[2] in string.digits)


