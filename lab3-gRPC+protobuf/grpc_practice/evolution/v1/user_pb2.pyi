from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "name", "nickname")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    nickname: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., nickname: _Optional[str] = ...) -> None: ...
