"""
   A Python 3.8 implementation of a model of wireless communication
   system between an aerial base station and two users.
   .. include:: ../README.md
   .. include:: ../doc/installationguide.md
   .. include:: ../doc/documentation.md
"""

from .generate_values import fading_rician
from .generate_values import random_position_uav
from .generate_values import random_position_users
from .generate_values import generate_channel
from .performance_metrics import calculate_instantaneous_rate_primary
from .performance_metrics import calculate_instantaneous_rate_secondary
from .performance_metrics import average_rate
from .performance_metrics import outage_probability

__pdoc__ = {}
__pdoc__["command_line.main"] = False
__pdoc__["command_line.validate"] = False