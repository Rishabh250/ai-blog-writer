from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
)
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

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


def get_llm(provider=None, model=None, **kwargs):
    """Get an LLM instance based on the specified provider and model.

    Args:
        provider: The LLM provider to use (gemini, openai, or anthropic)
        model: The specific model to use for the provider
        **kwargs: Additional arguments to pass to the LLM constructor

    Returns:
        An LLM instance
    """
    if provider is None:
        provider = settings.LLM_PROVIDER

    provider = provider.lower()

    if provider == "gemini":
        if model is None:
            model = settings.GEMINI_MODEL
        return ChatGoogleGenerativeAI(model=model, **kwargs)

    elif provider == "openai":
        if model is None:
            model = settings.OPENAI_MODEL
        return ChatOpenAI(model=model, api_key=settings.OPENAI_API_KEY, **kwargs)

    elif provider == "anthropic":
        if model is None:
            model = settings.ANTHROPIC_MODEL
        return ChatAnthropic(model=model, api_key=settings.ANTHROPIC_API_KEY, **kwargs)

    else:
        if model is None:
            model = settings.GEMINI_MODEL
        return ChatGoogleGenerativeAI(model=model, **kwargs)


def get_gemini_llm(model=settings.GEMINI_MODEL, **kwargs):
    """Get a Gemini LLM instance (for backward compatibility)."""
    return get_llm(provider="gemini", model=model, **kwargs)
