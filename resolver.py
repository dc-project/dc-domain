#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: ex_domain/resolver.py.py 
@time: 2017/11/6 16:56
"""

import json

from api import CloudXNS_API


class DomainRecorder(object):

    def __init__(self, api_key, secret_key, domain_suffix, domain_id):
        self.api_key = api_key
        self.secret_key = secret_key
        self.api = CloudXNS_API(self.api_key, self.secret_key, debug_log=True)

        self.domain_suffix = domain_suffix
        self.domain_id = domain_id

    def ping(self):
        body = self.api.domain_list()
        if isinstance(body, Exception):
            print(body)
            return False
        return True

    def exist_wild(self, name):
        host_id = self.get_host_id(name)
        return bool(host_id is not None)

    def get_host_id(self, name):
        host = '*.{}'.format(name)
        body = self.api.domain_host_list(self.domain_id, hostname=host)

        try:
            data = json.loads(body)
            if data['total'] != '0':
                return data["hosts"][0]["id"]
        except Exception as e:
            print(e)

        return None

    def add_wild(self, name, value, ttl=60):
        host = '*.{}'.format(name)
        body = self.api.domain_host_record_add(self.domain_id, host, value, 'A', '1', ttl=ttl)
        if body == '':
            return True
        else:
            print(body)
            return False

    def set_wild_record(self, name, records):
        host = '*.{}'.format(name)
        host_id = self.get_host_id(name)

        self.api.domain_host_delete(host_id)

        for record in records:
            self.api.domain_host_record_add(self.domain_id, host, record, 'A', '1', ttl=600)

    def del_wild(self, name):
        host_id = self.get_host_id(name)
        self.api.domain_host_delete(host_id)

    def update_wild(self, name, record):
        host = '*.{}'.format(name)
        host_id = self.get_host_id(name)
        self.api.domain_host_delete(host_id)
        body = self.api.domain_host_record_add(self.domain_id, host, record, 'A', '1', ttl=60)
        if body == '':
            return True
        else:
            return False
        return False
