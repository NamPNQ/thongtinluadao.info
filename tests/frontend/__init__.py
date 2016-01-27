# -*- coding: utf-8 -*-
"""
    tests.frontend
    ~~~~~~~~~~~~~~

    frontend tests package
"""

from .. import TTLDAppTestCase, settings


class TTLDFrontendTestCase(TTLDAppTestCase):

    def _create_app(self):
        from app import app
        return app

    def setUp(self):
        super(TTLDFrontendTestCase, self).setUp()
