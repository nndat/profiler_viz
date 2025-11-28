"""
Profiler Viz - A beautiful Python profiler with HTML visualization
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .profiler import func_profile
from .viewer import view_profile_html

__all__ = ['func_profile', 'view_profile_html']
