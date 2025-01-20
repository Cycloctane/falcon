"""General utilities.

This package includes multiple modules that implement utility functions
and classes that are useful to both apps and the Falcon framework
itself.

All utilities in the `structures`, `misc`, and `time` modules are
imported directly into the front-door `falcon` module for convenience::

    import falcon

    now = falcon.http_now()

Conversely, the `uri` module must be imported explicitly::

    from falcon import uri

    some_uri = '...'
    decoded_uri = uri.decode(some_uri)
"""

from http import cookies as http_cookies
import sys
from types import ModuleType

# Hoist misc. utils
from falcon.constants import PYTHON_VERSION
from falcon.util.deprecation import AttributeRemovedError
from falcon.util.deprecation import deprecated
from falcon.util.deprecation import deprecated_args
from falcon.util.deprecation import DeprecatedWarning
from falcon.util.mediatypes import parse_header
from falcon.util.misc import code_to_http_status
from falcon.util.misc import dt_to_http
from falcon.util.misc import get_argnames
from falcon.util.misc import get_bound_method
from falcon.util.misc import http_date_to_dt
from falcon.util.misc import http_now
from falcon.util.misc import http_status_to_code
from falcon.util.misc import is_python_func
from falcon.util.misc import secure_filename
from falcon.util.misc import to_query_str
from falcon.util.structures import CaseInsensitiveDict
from falcon.util.structures import Context
from falcon.util.structures import ETag
from falcon.util.sync import async_to_sync
from falcon.util.sync import create_task
from falcon.util.sync import get_running_loop
from falcon.util.sync import runs_sync
from falcon.util.sync import sync_to_async
from falcon.util.sync import wrap_sync_to_async
from falcon.util.sync import wrap_sync_to_async_unsafe
from falcon.util.time import TimezoneGMT

# NOTE(kgriffs, m-mueller): Monkey-patch support for the new 'Partitioned'
#   attribute that will probably be added in Python 3.14.
#   We do it this way because SimpleCookie does not give us a simple way to
#   specify our own subclass of Morsel.
_reserved_cookie_attrs = http_cookies.Morsel._reserved  # type: ignore[attr-defined]
if 'partitioned' not in _reserved_cookie_attrs:  # pragma: no cover
    _reserved_cookie_attrs['partitioned'] = 'Partitioned'
# NOTE(vytas): Partitioned is a boolean flag, similar to HttpOnly and Secure.
http_cookies.Morsel._flags.add('partitioned')  # type: ignore[attr-defined]
# NOTE(vytas): Morsel._reserved_defaults is a new optimization in Python 3.14+
#   for faster initialization of Morsel instances.
# TODO(vytas): Remove this part of monkey-patching in the case CPython 3.14
#   adds the Partitioned attribute to Morsel.
_reserved_cookie_defaults = getattr(http_cookies.Morsel, '_reserved_defaults', None)
if (
    _reserved_cookie_defaults is not None
    and 'partitioned' not in _reserved_cookie_defaults
):  # pragma: no cover
    _reserved_cookie_defaults['partitioned'] = ''


IS_64_BITS = sys.maxsize > 2**32

from falcon.util.reader import BufferedReader as _PyBufferedReader  # NOQA

try:
    from falcon.cyutil.reader import BufferedReader as _CyBufferedReader
except ImportError:
    _CyBufferedReader = None

# NOTE(vytas): Cythonized BufferedReader makes heavy use of Py_ssize_t which
#   would overflow on 32-bit systems with form parts larger than 2 GiB.
BufferedReader = (
    (_CyBufferedReader or _PyBufferedReader) if IS_64_BITS else _PyBufferedReader
)
