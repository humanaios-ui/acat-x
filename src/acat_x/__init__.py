"""ACAT-X: Inspect AI evaluation suite for behavioral assessment and calibration."""

__version__ = "0.1.0"
__author__ = "HumanAIOS"

from .consist import acat_x_consist
from .truth import acat_x_truth

__all__ = [
    "acat_x_consist",
    "acat_x_truth",
]
