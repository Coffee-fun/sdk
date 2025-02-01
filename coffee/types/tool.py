from typing import Annotated, Literal, Optional

from pydantic import BaseModel, HttpUrl, StringConstraints

from ..config import config

from ..log import logger


class PluginArgType(BaseModel):
    type: Literal["string", "number", "integer", "object", "array", "boolean", "null"]
    description: Optional[str] = None


class PluginIn(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=64,
            pattern="^[a-zA-Z0-9_-]+$",
        ),
    ]
    description: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=1024,
        ),
    ]
    about: Optional[str]
    url: Optional[HttpUrl] = None
    args: dict[str, PluginArgType]


class RemoteTool(BaseModel):
    name: str
    url: str
    args: dict[str, PluginArgType]
    instructions: str
    tool_id: str

    _is_registered: bool = False

    def register_tool(self):
        if self._is_registered:
            return
        logger.debug(f"Registering <Tool={self.name=}, {self.url=}")
        config.api_client.create_plugin(self.model_dump(mode="json"))
        self._is_registered = True
