from typing import Any

import click
from ape.exceptions import ApeException

from .types import TaskType


class ImportFromStringError(Exception):
    pass


class InvalidContainerTypeError(Exception):
    def __init__(self, container: Any):
        super().__init__(f"Invalid container type: {container.__class__}")


class InvalidContainerConfigurationError(Exception):
    pass


class UnregisteredTask(Exception):
    def __init__(self, task_name: str):
        super().__init__(f"Could not find task '{task_name}'.")


class ContainerTypeMismatchError(Exception):
    def __init__(self, task_type: TaskType, container: Any):
        super().__init__(f"Invalid container type for '{task_type}': {container.__class__}")


class NoWebsocketAvailableError(Exception):
    def __init__(self):
        super().__init__(
            "Attempted to a use WebsocketRunner without a websocket-compatible provider."
        )


class SilverbackException(ApeException):
    """Base Exception for any Silverback runtime faults."""


class NoSignerLoaded(SilverbackException):
    def __init__(self):
        super().__init__(
            "No signer was made available. Please check config (e.g. `SILVERBACK_SIGNER_ALIAS=...`)"
        )


# TODO: `ExceptionGroup` added in Python 3.11
class StartupFailure(SilverbackException, click.ClickException):
    def __init__(self, *exceptions: BaseException | str | None):
        if len(exceptions) == 1 and isinstance(exceptions[0], str):
            super().__init__(exceptions[0])
        elif error_str := "\n".join(str(e) for e in exceptions):
            super().__init__(f"Startup failure(s):\n{error_str}")
        else:
            super().__init__("Startup failure(s) detected. See logs for details.")


class NoTasksAvailableError(StartupFailure):
    def __init__(self):
        super().__init__("No tasks to execute")


class Halt(SilverbackException):
    def __init__(self):
        super().__init__("Bot halted, must restart manually")


class CircuitBreaker(Halt):
    """Custom exception (created by user) that will trigger an bot shutdown."""

    def __init__(self, message: str):
        super(SilverbackException, self).__init__(message)


# For Silverback Cluster client commands (CLI)
# NOTE: Subclass `click.UsageError` here so bad requests in CLI don't show stack trace
class ClientError(SilverbackException, click.UsageError):
    """Exception for client errors in the HTTP request."""
