# -*- coding: utf-8 -*-
"""
    tests.factories
    ~~~~~~~~~~~~~~~

    TTLD test factories module
"""

from datetime import datetime

from factory import Factory, Sequence, LazyAttribute


class UserFactory(Factory):
    email = Sequence(lambda n: 'user{0}@gmail.com'.format(n))
