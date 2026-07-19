"""Re-export of the DB dependency, kept here so imports like
`from dependencies.database_dependency import get_db` (used by controllers) work."""
from database.connection import get_db  # noqa: F401
