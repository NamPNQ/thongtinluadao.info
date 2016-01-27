# -*- coding: utf-8 -*-
"""
    tests
    ~~~~~

    tests package
"""

from unittest import TestCase

from .factories import UserFactory
from .utils import FlaskTestCaseMixin


class TTLDTestCase(TestCase):
    pass


class TTLDAppTestCase(FlaskTestCaseMixin, TTLDTestCase):

    def _create_app(self):
        raise NotImplementedError

    def _create_fixtures(self):
        self.user = UserFactory()

    def setUp(self):
        super(TTLDAppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        # self._create_fixtures()
        # self._create_csrf_token()

    def tearDown(self):
        super(TTLDAppTestCase, self).tearDown()
        self.app_context.pop()
