from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
)
from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings

_SESSION_MEMORIES = {}


class SessionMemory(ConversationBufferMemory):
    """Extended ConversationBufferMemory that can store session data."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._session_data = {}

    def set_session_data(self, key, value):
        """Store arbitrary data in session memory."""
        self._session_data[key] = value

    def get_session_data(self, key, default=None):
        """Retrieve arbitrary data from session memory."""
        return self._session_data.get(key, default)

    def get_all_session_data(self):
        """Get all session data."""
        return self._session_data


class SessionWindowMemory(ConversationBufferWindowMemory):
    """Extended ConversationBufferWindowMemory that can store session data."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._session_data = {}

    def set_session_data(self, key, value):
        """Store arbitrary data in session memory."""
        self._session_data[key] = value

    def get_session_data(self, key, default=None):
        """Retrieve arbitrary data from session memory."""
        return self._session_data.get(key, default)

    def get_all_session_data(self):
        """Get all session data."""
        return self._session_data


def get_memory(session_id=None, memory_type=None, k=None):
    """Get a memory instance based on the specified type.

    Args:
        session_id: Optional session identifier to retrieve existing memory
        memory_type: Type of memory to use ("buffer" or "buffer_window")
        k: Number of messages to keep in window memory

    Returns:
        A memory instance
    """
    if session_id and session_id in _SESSION_MEMORIES:
        return _SESSION_MEMORIES[session_id]

    if memory_type is None:
        memory_type = settings.MEMORY_TYPE

    if k is None:
        k = settings.MEMORY_WINDOW_SIZE

    if memory_type.lower() == "buffer_window":
        memory = SessionWindowMemory(
            k=k, return_messages=True, memory_key="chat_history"
        )
    else:
        memory = SessionMemory(return_messages=True, memory_key="chat_history")

    if session_id:
        _SESSION_MEMORIES[session_id] = memory

    return memory


def clear_memory(session_id):
    """Clear memory for a specific session.

    Args:
        session_id: Session identifier to clear

    Returns:
        True if memory was found and cleared, False otherwise
    """
    if session_id in _SESSION_MEMORIES:
        _SESSION_MEMORIES[session_id].clear()
        return True
    return False


def get_gemini_llm(model=settings.LLM_MODEL, **kwargs):
    """Get a Gemini LLM instance."""
    return ChatGoogleGenerativeAI(model=model, **kwargs)
