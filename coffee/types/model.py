from typing import Optional

from pydantic import BaseModel, Field


class Model(BaseModel):
    id: str = Field(..., alias="model")
    name: Optional[str] = None
    provider: Optional[str] = Field(None, validate_default=True)


class OpenAI(Model):
    id: str = "gpt-4o"
    name: str = "OpenAIChat"
    provider: str = "OpenAI"


class DeepSeekChat(OpenAI):
    id: str = "deepseek-chat"
    name: str = "DeepSeekChat"
    provider: str = "DeepSeek"
    base_url: str = "https://api.deepseek.com"


class Claude(Model):
    id: str = "claude-3-5-sonnet-20241022"
    name: str = "Claude"
    provider: str = "Anthropic"


# MIGHT NOT WORK
class xAI(OpenAI):
    id: str = "grok-beta"
    name: str = "xAI"
    provider: str = "xAI"
    base_url: Optional[str] = "https://api.x.ai/v1"


class Groq(Model):
    id: str = "llama3-groq-70b-8192-tool-use-preview"
    name: str = "Groq"
    provider: str = "Groq"
