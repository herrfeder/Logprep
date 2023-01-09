"""
RawstringlInput
==========
A json line input that returns the documents it was initialized with.
If a "document" is derived from BaseException, that exception will be thrown instead of
returning a document. The exception will be removed and subsequent calls may return documents or
throw other exceptions in the given order.
Example
^^^^^^^
..  code-block:: yaml
    :linenos:
    input:
      myrawstringlinput:
        type: rawstringl_input
        documents_path: path/to/a/document
"""
from functools import cached_property

from logprep.connector.dummy.input import DummyInput
from logprep.util.rawstring_handling import parse_rawstring


class RawstringlInput(DummyInput):
    """RawstringlInput Connector"""

    @define(kw_only=True)
    class Config(Input.Config):
        """RawstringlInput connector specific configuration"""

        documents_path: str
        """A path to a file in generic raw format, which can be in any string based format. Needs to be parsed with normalizer"""

    @cached_property
    def _documents(self):
        return parse_rawstring(self._config.documents_path)

