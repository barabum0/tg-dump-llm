import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field


class TelegramMessage(BaseModel):
    id: int
    type: Literal["message"] = "message"
    date: datetime.datetime
    author_name: Annotated[str, Field(validation_alias="from")]
    author_id: Annotated[str, Field(validation_alias="from_id")]
    text_entities: list[dict[str, Any]]

    @property
    def text(self) -> str:
        return "".join(t.get("text", "") for t in self.text_entities)


class TelegramDump(BaseModel):
    name: str
    messages: list[TelegramMessage]
