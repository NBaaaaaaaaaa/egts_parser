from enum import Enum


# Сервисы, поддерживаемые протоколом.
class Types_text(Enum):
    CONNECTED = 1
    DISCONNECTED = 2
    ERROR = 3
    SENT_DATA = 4
    PROCESSED_SUCCESSFULLY = 5
