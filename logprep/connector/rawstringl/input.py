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

from attrs import define

from logprep.abc.input import Input
from logprep.connector.dummy.input import DummyInput
from logprep.util.rawstring_handling import parse_rawstring
import time
from typing import Iterator


import threading 
import time

class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False


class RawstringlInput(Input):
    """RawstringlInput Connector"""
    

    @define(kw_only=True)
    class Config(Input.Config):
        """RawstringlInput connector specific configuration"""

        documents_path: str
        """A path to a file in generic raw format, which can be in any string based format. Needs to be parsed with normalizer"""


    @property
    def _documents(self):
        return self._follow()
   
    

    def _follow(self, sleep_sec=1, exit_end=False) -> Iterator[str]: 
        """ Yield each line from a file as they are written.
        `sleep_sec` is the time to sleep after empty reads. """
        with open(self._config.documents_path) as file:
            while True:
                line = file.readline()
                if line is not '':
                    if line.endswith("\n"):
                        yield line
                        line = ''
                
                elif exit_end:
                    break
                elif sleep_sec:
                    time.sleep(sleep_sec)


    def _get_event(self, timeout: float) -> tuple:
        """Retrieve next document from configuration and raise error if found"""
        if not self._documents:
            raise SourceDisconnectedError

        document = next(self._documents)

        if (document.__class__ == type) and issubclass(document, BaseException):
            raise document
        return document, None

