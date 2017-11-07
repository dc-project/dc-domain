#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: ex_domain/domain.py 
@time: 2017/11/7 11:29
"""

import sys
import argparse
from resolver import DomainRecorder
from tools import make_wild_name, is_passive_wild_name
from interaction import Input
from config import Config

api_key = Config.api_key
secret_key = Config.secret_key
domain_suffix = Config.domain_suffix
domain_id = Config.domain_id
resolver = DomainRecorder(api_key=api_key, secret_key=secret_key, domain_suffix=domain_suffix, domain_id=domain_id)


def do_stdout(arg, end=True):
    sys.stdout.write('{}'.format(arg))
    if end:
        sys.stdout.write("\n")
    sys.stdout.flush()


class ExDomain(object):

    def __init__(self, parse_args, *args, **kwargs):
        self.ip = parse_args.ip


    def get_random_suffix(self):
        dr = DomainRecorder(api_key=api_key, secret_key=secret_key, domain_suffix=domain_suffix, domain_id=domain_id)
        for count in range(5):
            new_suffix = make_wild_name()
            if dr.exist_wild(new_suffix):
                print("exist wild_suffix {}, retry.".format(new_suffix))
                continue
            else:
                return new_suffix
        print("unlucky, test 5 wild_domain failed, please try again.")
        return None

    @classmethod
    def init_domain(cls, parse_args):
        obj = cls(parse_args)
        if resolver.ping() is False:
            print("looks like I can't access internet....")
            input_domain = Input.read("Setup wild_domain for this region,like '<name>.goodrain.org'", blank=False)
        else:
            input_domain = Input('', is_blank=True)

        if input_domain.is_blank:
            suffix = obj.get_random_suffix()
            if suffix is None:
                return 1

            resolver.add_wild(suffix, parse_args.ip)
            if resolver.exist_wild(suffix):
                print("prepare domain *.{}.goodrain.org finished".format(suffix))
                web_domain = '{}.goodrain.org'.format(suffix)
            else:
                print("prepare domain *.{}.goodrain.org failed,retry".format(suffix))
        else:
            if input_domain.value.endswith('.goodrain.org'):
                suffix = input_domain.value.replace('.goodrain.org', '').lstrip('*.')
                try:
                    if is_passive_wild_name(suffix):
                        web_domain = '{}.goodrain.org'.format(suffix)
                except Exception as e:
                    print(e)
                    return 1
            else:
                print("Use custom domain:{}".format(input_domain.value))
                web_domain = input_domain.value

        print("init successful:{}".format(web_domain))
        return 0

    @classmethod
    def del_domain(cls, parse_args):
        if parse_args.domain.endswith('.goodrain.org'):
            suffix = parse_args.domain.replace('.goodrain.org', '').lstrip('*.')
        else:
            suffix = parse_args.domain.lstrip('*.')
        if resolver.exist_wild(suffix):
            print("delete domain:{}.goodrain.org".format(suffix))
            resolver.del_wild(suffix)
            if resolver.exist_wild(suffix):
                print("delete failed...")
                return 0
            print("delete sucessful:{}.goodrain.org".format(suffix))
        else:
            print("domain {}.goodrain.org not exist.".format(suffix))

    @classmethod
    def update_domain(cls, parse_args):
        if parse_args.domain.endswith('.goodrain.org'):
            suffix = parse_args.domain.replace('.goodrain.org', '').lstrip('*.')
        else:
            suffix = parse_args.domain.lstrip('*.')
        if resolver.exist_wild(suffix):
            print("update domain:{}.goodrain.org".format(suffix))
            resolver.update_wild(suffix, parse_args.ip)
            if resolver.exist_wild(suffix):
                print("update sucessful:{}.goodrain.org --> {}".format(suffix, parse_args.ip))
                return 0
            print("update failed...")
        else:
            print("domain {}.goodrain.org not exist.".format(suffix))


def main():
    parser = argparse.ArgumentParser(description="Goodrain Domain DC-Tools")
    subparsers = parser.add_subparsers(metavar='<subcommand>')
    init_command = subparsers.add_parser('init', help='init domain resolve')
    init_command.add_argument('--ip', action='store', default='127.0.0.1')
    init_command.set_defaults(func=ExDomain.init_domain)

    del_command = subparsers.add_parser('del', help='del domain resolve')
    del_command.add_argument('--domain', action='store', default=None, help='just like www.google.com')
    del_command.set_defaults(func=ExDomain.del_domain)

    update_command = subparsers.add_parser('update', help='update domain resolve')
    update_command.add_argument('--ip', action='store', default='127.0.0.1')
    update_command.add_argument('--domain', action='store', default=None, help='just like www.google.com')
    update_command.set_defaults(func=ExDomain.update_domain)

    args = parser.parse_args()

    """
    stdout args
    """
    # do_stdout(args)

    if hasattr(args, 'func') and args.func is not None:
        args.func(args)
    else:
        print("<subcommand> choose from 'init', 'del', 'update'.")
        print("Thank you.")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("exit...")
