import io

import pytest

import falcon.uri
import falcon.util


class TestCythonized:
    def test_imported_from_c_modules(self, util):
        if not util.HAS_CYTHON:
            pytest.skip(reason='Cython not installed')

        assert 'cyfunction' in str(falcon.uri.parse_query_string)

    def test_stream_has_private_read(self, util):
        stream = falcon.util.BufferedReader(io.BytesIO().read, 8)

        if util.HAS_CYTHON and falcon.util.IS_64_BITS:
            assert not hasattr(stream, '_read')
        else:
            assert hasattr(stream, '_read')
