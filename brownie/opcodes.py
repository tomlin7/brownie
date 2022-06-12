import json
from dataclasses import dataclass
from typing import Literal

@dataclass
class Operand:
    immediate: bool
    name: str
    bytes: int = None
    value: int = None
    adjust: Literal["+", "-"] = None

    def create(self, value):
        return Operand(immediate=self.immediate, name=self.name,
            bytes=self.bytes, value=value, adjust=self.adjust)
    
    def print(self):
        if self.adjust is None:
            adjust = ""
        else:
            adjust = self.adjust
        if self.value is not None:
            if self.bytes is not None:
                val = hex(self.value)
            else:
                val = self.value
            v = val
        else:
            v = self.name
        v = v + adjust
        if self.immediate:
            return v
        return f'({v})'


@dataclass
class Instruction:
    opcode: int
    immediate: bool
    operands: list[Operand]
    cycles: list[int]
    bytes: int
    mnemonic: str
    comment: str = ""

    def create(self, operands):
        return Instruction(opcode=self.opcode, immediate=self.immediate,
            operands=operands, cycles=self.cycles, bytes=self.bytes,
            mnemonic=self.mnemonic, comment=self.comment)

instructions = []
with open('brownie/etc/opcodes.json') as f:
    opcodes = json.load(f)
    for opcode, details in opcodes['unprefixed'].items():
        details.pop('flags', None)

        operands = []
        for op in details['operands']:
            if incr := op.pop('increment', False):
                op['adjust'] = '+' if incr else '-'
            if decr := op.pop('decrement', False):
                op['adjust'] = '-' if decr else '+'
            operands.append(Operand(**op))
        details['operands'] = operands
        
        instruction = Instruction(int(opcode, base=16), **details)
        instructions.append(instruction)

print(instructions[0xFF])

