"""In-memory event store for MCP server sessions."""

from mcp.server.streamable_http_manager import EventStore


class InMemoryEventStore(EventStore):
    """In-memory implementation of EventStore for MCP sessions.

    This allows clients to resume connections and receive missed events.
    Events are stored in memory per session.
    """

    def __init__(self) -> None:
        """Initialize the in-memory event store."""
        self._events: dict[str, list[str]] = {}

    async def store_event(self, session_id: str, event: str) -> None:
        """Store an event for a given session.

        Args:
            session_id: The session identifier
            event: The event data to store
        """
        if session_id not in self._events:
            self._events[session_id] = []
        self._events[session_id].append(event)

    async def get_events(self, session_id: str, after_sequence: int) -> list[str]:
        """Retrieve events for a session after a given sequence number.

        Args:
            session_id: The session identifier
            after_sequence: Get events after this sequence number

        Returns:
            List of events after the given sequence
        """
        if session_id not in self._events:
            return []
        return self._events[session_id][after_sequence:]

    async def delete_session(self, session_id: str) -> None:
        """Delete all events for a session.

        Args:
            session_id: The session identifier
        """
        if session_id in self._events:
            del self._events[session_id]
