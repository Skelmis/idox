__version__ = "0.1.1"

import logging
from collections import namedtuple

from idox.structs import Request
from idox.sequences import SequenceT, NumericSequence, FileSequence
from idox.exceptions import BaseIdoxException, MalformedRequest
from idox.idox import Idox

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=0, minor=1, micro=1, releaselevel="beta", serial=0)
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = (
    "Request",
    "BaseIdoxException",
    "MalformedRequest",
    "Idox",
    "SequenceT",
    "NumericSequence",
    "FileSequence",
)
