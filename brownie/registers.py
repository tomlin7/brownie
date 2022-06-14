from collections.abc import MutableMapping
from dataclasses import dataclass

__all__ = ["Registers", "FLAGS", "REGISTERS_HIGH", "REGISTERS_LOW", "REGISTERS"]

REGISTERS_LOW = {
    "F": "AF",
    "C": "BC",
    "E": "DE",
    "L": "HL",
}
REGISTERS_HIGH = {
    "A": "AF",
    "B": "BC",
    "D": "DE",
    "H": "HL"
}
REGISTERS = {
    "AF", "BC", "DE", "HL", "PC", "SP", 
}
FLAGS = {
    "c": 4,
    "h": 5,
    "n": 6,
    "z": 7,
}


@dataclass
class Registers(MutableMapping):
    AF: int = 0
    BC: int = 0
    DE: int = 0
    HL: int = 0
    PC: int = 0
    SP: int = 0

    def values(self):
        return [self.AF, self.BC, self.DE, self.HL, self.PC, self.SP]

    def __iter__(self):
        return iter(self.values())
    
    def __len__(self):
        return len(self.values())
    
    def __getitem__(self, key):
        if register := REGISTERS_HIGH.get(key, None):
            return self.__getattribute__(register) >> 8
        elif register := REGISTERS_LOW.get(key, None):
            return self.__getattribute__(register) & 0xFF
        elif register := FLAGS.get(key, None):
            return (self.AF >> register) & 1
        else:
            if key in REGISTERS:
                return getattr(self, key)
            else:
                raise KeyError(f"No such register {key}")
    
    def __setitem__(self, key, value):
        if register := REGISTERS_HIGH.get(key, None):
            current_value = self[register]
            setattr(self, register, (current_value & 0x00FF | (value << 8)) & 0xFFFF)
        elif register := REGISTERS_LOW.get(key, None):
            current_value = self[register]
            setattr(self, register, (current_value & 0xFF00 | value) & 0xFFFF)
        elif register := FLAGS.get(key, None):
            assert value in (0, 1), f"{value} must be 0 or 1"
            flag_bit = FLAGS[key]
            if not value:
                self.AF &= ~(1 << flag_bit)
            else:
                self.AF |= (1 << flag_bit)
        else:
            if key in REGISTERS:
                setattr(self, key, value & 0xFFFF)
            else:
                raise KeyError(f"No such register {key}")
    
    def __delitem__(self, key):
        raise NotImplementedError("Register deletion is not supported")
