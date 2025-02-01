from .types.model import (
    OpenAI as OpenAI,
    Claude as Claude,
    DeepSeekChat as DeepSeekChat,
    Groq as Groq,
    xAI as xAI,
)

DEFAULT_MODEL = OpenAI(id="gpt-4o")
