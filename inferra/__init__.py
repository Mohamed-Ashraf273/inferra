# This file should NEVER be packaged!

import os  # isort: skip

# Add everything in /api/ to the module search path.
__path__.append(os.path.join(os.path.dirname(__file__), "api"))  # noqa: F405

from inferra.api import *  # noqa: F403, E402
from inferra.api import __version__  # noqa: E402

# Don't pollute namespace.
del os
