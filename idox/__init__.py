__version__ = "0.1.1"

import logging
from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=0, minor=1, micro=1, releaselevel="beta", serial=0)
logging.getLogger(__name__).addHandler(logging.NullHandler())

from idox.structs import Request
from idox.sequences import SequenceT, NumericSequence
from idox.exceptions import BaseIdoxException, MalformedRequest
from idox.idox import Idox

__all__ = (
    "Request",
    "BaseIdoxException",
    "MalformedRequest",
    "Idox",
    "SequenceT",
    "NumericSequence",
)
