"""
data package manages dynamic configurations through Google datastore.
This package is referenced from other packages under 'app', so this should not depend on those packages.
"""
from .data import get_config, put_config
