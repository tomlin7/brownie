from dataclasses import dataclass
from typing import Literal


@dataclass
class Operand:
    immediate: bool
    name: str
    bytes: int = None
    value: int = None
    adjust: Literal["+", "-"] = None

    def copy(self, value):
        return Operand(immediate=self.immediate, name=self.name,
            bytes=self.bytes, value=value, adjust=self.adjust)
    
    def print(self):
        adjust = self.adjust or ""
        v = (hex(self.value) if self.bytes else self.value) if self.value else self.name
        v = v + adjust
        
        if self.immediate:
            return v
        return f"({v})"
