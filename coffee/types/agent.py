from typing import Annotated, Any, Optional, Union, Literal

from pydantic import BaseModel, StringConstraints

from .model import Model, OpenAI
from .tool import RemoteTool

DEFAULT_MODEL = OpenAI(id="gpt-4o")
StringNoSpacesNoSpecialChars = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=64,
        pattern="^[a-zA-Z0-9_-]+$",
    ),
]
BuiltinTools = Literal[
    "web3_essentials_tools",
    "solana_tools",
    "eth_tools",
    "calculator",
    "crawl4ai_tools",
    "csv_tools",
    "dalle",
    "duckdb_tools",
    "duckduckgo",
    "elevenlabs_tools",
    "googlesearch",
    "hackers_news",
    "jina_reader_tools",
    "newspaper_tools",
    "pubmed",
    "replicate_toolkit",
    "spider",
    "web_browser",
    "wikipedia_tools",
    "yfinance_tools",
    "youtube_tools",
    "giphy_tools",
    "sleep",
]


class AgentIn(BaseModel):
    name: StringNoSpacesNoSpecialChars
    guidelines: Optional[list[str]] = None
    instructions: Optional[Union[list[str], str]] = None
    short_description: Optional[str] = None
    tools: list[Union[BuiltinTools, RemoteTool]] = []
    model: Model = DEFAULT_MODEL
    team: list[Any] = []
    imageUrl: str = "https://tivzaxmpxiyucjvvdtko.supabase.co/storage/v1/object/public/coffee-pre-prod-2025/default.png"
    session_id: Optional[str] = None
    agent_id: Optional[str] = None
