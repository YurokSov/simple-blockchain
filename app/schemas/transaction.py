from typing import Union
from pydantic import BaseModel

class BaseMessage(BaseModel):
    type: str

class TransferMessage(BaseMessage):
    object: str
    amount: int

class ContentMessage(BaseMessage):
    content: str

class Transaction(BaseModel):
    source: str
    destination: str
    message: Union[TransferMessage, ContentMessage]