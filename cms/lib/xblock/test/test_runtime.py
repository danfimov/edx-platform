"""
Tests of edX Studio runtime functionality
"""


from unittest import TestCase
from urllib.parse import urlparse

from unittest.mock import Mock

from cms.lib.xblock.runtime import handler_url


class TestHandlerUrl(TestCase):
    """Test the LMS handler_url"""

    def setUp(self):
        super().setUp()
        self.block = Mock()

    def test_trailing_characters(self):
        assert not handler_url(self.block, 'handler').endswith('?')
        assert not handler_url(self.block, 'handler').endswith('/')

        assert not handler_url(self.block, 'handler', 'suffix').endswith('?')
        assert not handler_url(self.block, 'handler', 'suffix').endswith('/')

        assert not handler_url(self.block, 'handler', 'suffix', 'query').endswith('?')
        assert not handler_url(self.block, 'handler', 'suffix', 'query').endswith('/')

        assert not handler_url(self.block, 'handler', query='query').endswith('?')
        assert not handler_url(self.block, 'handler', query='query').endswith('/')

    def _parsed_query(self, query_string):
        """Return the parsed query string from a handler_url generated with the supplied query_string"""
        return urlparse(handler_url(self.block, 'handler', query=query_string)).query

    def test_query_string(self):
        self.assertIn('foo=bar', self._parsed_query('foo=bar'))
        self.assertIn('foo=bar&baz=true', self._parsed_query('foo=bar&baz=true'))
        self.assertIn('foo&bar&baz', self._parsed_query('foo&bar&baz'))

    def _parsed_path(self, handler_name='handler', suffix=''):
        """Return the parsed path from a handler_url with the supplied handler_name and suffix"""
        return urlparse(handler_url(self.block, handler_name, suffix=suffix)).path

    def test_suffix(self):
        assert self._parsed_path(suffix="foo").endswith('foo')
        assert self._parsed_path(suffix="foo/bar").endswith('foo/bar')
        assert self._parsed_path(suffix="/foo/bar").endswith('/foo/bar')

    def test_handler_name(self):
        self.assertIn('handler1', self._parsed_path('handler1'))
        self.assertIn('handler_a', self._parsed_path('handler_a'))
