"""
data package manages dynamic configurations through mongodb.
This package is referenced from other packages under 'more_one_memo', so this should not depend on those packages.
"""
from .data import get_user_config_optional, get_user_config, upsert_user_config  # noqa: F401
