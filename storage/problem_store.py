"""Problem library storage interface.

The UI is ready for a future cloud backend, but this module intentionally does
not persist data yet. When authentication and cloud storage are added, implement
these functions with the selected backend, such as Supabase.
"""


class CloudStorageNotConfiguredError(NotImplementedError):
    """Raised when a cloud storage operation is requested before setup."""


def list_folders(user_id: str):
    """Return folders for a user after cloud storage is configured."""
    raise CloudStorageNotConfiguredError("Cloud problem storage is not configured yet.")


def create_folder(user_id: str, name: str):
    """Create a folder for a user after cloud storage is configured."""
    raise CloudStorageNotConfiguredError("Cloud problem storage is not configured yet.")


def save_problem(user_id: str, folder_id: str, problem_data: dict):
    """Save generated problem data after cloud storage is configured."""
    raise CloudStorageNotConfiguredError("Cloud problem storage is not configured yet.")


def list_problems(user_id: str, folder_id: str | None = None):
    """Return saved problems for a user after cloud storage is configured."""
    raise CloudStorageNotConfiguredError("Cloud problem storage is not configured yet.")


def get_problem(user_id: str, problem_id: str):
    """Return one saved problem after cloud storage is configured."""
    raise CloudStorageNotConfiguredError("Cloud problem storage is not configured yet.")
