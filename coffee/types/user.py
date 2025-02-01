from typing import Optional

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id_: str
    user_name: str
    name: str
    is_admin: bool
    avatar_url: Optional[str] = None


class CurrentUser(UserOut):
    secure: dict = Field(alias="_secure_")
