__version__ = "1.3.3"

import logging
from collections import namedtuple

from idox.case_insensitive_dict import CaseInsensitiveDict
from idox.exceptions import BaseIdoxException, MalformedRequest, MalformedResponse
from idox.structs import Request, Response
from idox.sequences import SequenceT, NumericSequence, FileSequence
from idox.idox import Idox

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=1, minor=4, micro=0, releaselevel="stable", serial=0)
logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = (
    "CaseInsensitiveDict",
    "BaseIdoxException",
    "MalformedResponse",
    "MalformedRequest",
    "Request",
    "Response",
    "Idox",
    "SequenceT",
    "NumericSequence",
    "FileSequence",
)
