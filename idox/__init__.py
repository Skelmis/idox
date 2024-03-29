__version__ = "0.0.1"

import logging
from collections import namedtuple

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=0, minor=0, micro=1, releaselevel="alpha", serial=0)
logging.getLogger(__name__).addHandler(logging.NullHandler())