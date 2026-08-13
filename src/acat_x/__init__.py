"""ACAT-X: Inspect AI evaluation suite for behavioral assessment and calibration."""

__version__ = "0.1.0"
__author__ = "HumanAIOS"

# Core dimensions (6)
from .consist import acat_x_consist
from .truth import acat_x_truth
from .sycophancy import acat_x_sycophancy
from .harm import acat_x_harm
from .service import acat_x_service
from .autonomy import acat_x_autonomy
from .value import acat_x_value
from .humility import acat_x_humility

# Candidate dimensions (6)
from .handoff import acat_x_handoff
from .calibration import acat_x_calibration
from .boundary import acat_x_boundary
from .transparency import acat_x_transparency
from .temporal import acat_x_temporal
from .drift import acat_x_drift

__all__ = [
    # Core dimensions
    "acat_x_consist",
    "acat_x_truth",
    "acat_x_sycophancy",
    "acat_x_harm",
    "acat_x_service",
    "acat_x_autonomy",
    "acat_x_value",
    "acat_x_humility",
    # Candidate dimensions
    "acat_x_handoff",
    "acat_x_calibration",
    "acat_x_boundary",
    "acat_x_transparency",
    "acat_x_temporal",
    "acat_x_drift",
]
