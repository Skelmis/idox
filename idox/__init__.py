__version__ = "1.2.0"

import logging
from collections import namedtuple

from idox.exceptions import BaseIdoxException, MalformedRequest
from idox.structs import Request
from idox.sequences import SequenceT, NumericSequence, FileSequence
from idox.idox import Idox

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=1, minor=3, micro=0, releaselevel="beta", serial=0)
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = (
    "BaseIdoxException",
    "MalformedRequest",
    "Request",
    "Idox",
    "SequenceT",
    "NumericSequence",
    "FileSequence",
)
