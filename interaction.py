class Input(object):

    @classmethod
    def read(cls, desc, default=None, blank=True, choices=()):
        if choices:
            choose = '|'.join(choices)
            desc = '{} ({})'.format(desc, choose)
            blank = False
        if default is not None:
            desc = '{} [{}]'.format(desc, default)
            blank = True

        desc = '{} : '.format(desc)
        value = ''
        is_blank = None

        while True:
            user_input = input(desc)
            if len(user_input) == 0:
                if blank:
                    value = default if default is not None else user_input
                    is_blank = True
                    break
                else:
                    print("need some input, retry")
                    continue
            else:
                if choices:
                    if user_input not in choices:
                        print("need input one of ({})".format(choose))
                        continue
                value = user_input
                is_blank = False
                break
        return cls(value, is_blank=is_blank)

    def __init__(self, value, is_blank):
        self.value = value
        self.is_blank = is_blank

    def __str__(self):
        return 'input is {}'.format(self.value)

    def __repr__(self):
        return 'input is {}'.format(self.value)

if __name__ == '__main__':
    m = Input.read("give input", default='a', choices=('a', 'b'))
    print(m)