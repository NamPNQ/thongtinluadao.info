# -*- coding: utf-8 -*-
"""
    tests.frontend.index_tests
    ~~~~~~~~~~~~~~~~~~~~

    frontend index tests module
"""

from . import TTLDFrontendTestCase


class IndexTestCase(TTLDFrontendTestCase):

    def test_page_title(self):
        r = self.get('/')
        self.assertOk(r)
        self.assertIn('<title>Thongtinluadao', r.data)
