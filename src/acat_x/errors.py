"""Custom error taxonomy for ACAT-X evaluation flows."""

from __future__ import annotations


class AcatError(Exception):
    """Base exception for ACAT-X."""


class ConfigurationError(AcatError):
    """Raised when runtime configuration is invalid."""


class ModelInvocationError(AcatError):
    """Raised when a model provider invocation fails."""


class TaskLoadError(AcatError):
    """Raised when an ACAT-X task cannot be imported or instantiated."""


class DatasetError(AcatError):
    """Raised when dataset extraction fails or yields no samples."""


class EvaluationExecutionError(AcatError):
    """Raised when evaluation execution fails unexpectedly."""
